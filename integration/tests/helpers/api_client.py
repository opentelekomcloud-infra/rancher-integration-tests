import logging
import time

import requests
from pyasli import BrowserSession
from requests import Session

from integration.tests.helpers.timeouts import CLUSTER_DELETED, DRIVER_ACTIVATING

CCE_DRIVER_NAME = 'otccce'
LOGGER = logging.getLogger('helpers.api')


class APIClient:
    """Client for rancher API"""

    def __init__(self, base_url):
        self.session = requests.session()

        def _request(method, url, *args, **kwargs):
            if len(url.split('://')) == 1:  # if not absolute URL
                url = base_url + url
            return Session.request(self.session, method, url, *args, **kwargs)

        self.session.request = _request

    @classmethod
    def from_browser_session(cls, browser: BrowserSession):
        """Create new API Client from browser session instance"""
        instance = cls(browser.base_url)
        cookies = browser.get_actual().get_cookies()
        sess = instance.session
        sess.verify = False
        sess.cookies.update({c['name']: c['value'] for c in cookies})
        sess.headers = {'X-API-CSRF': sess.cookies.get('CSRF')}
        instance.session = sess
        LOGGER.debug('Created new API session from browser session')
        return instance

    _cluster_driver_list_url = '/v3/kontainerDrivers'
    _cluster_list_url = '/v3/clusters'
    _cluster_driver_url = '/v3/kontainerDrivers/{id}'

    def create_cluster_driver(self, url, ui_url, domains):
        """Register OTC CCE driver

        :return: created driver ID
        """
        data = {
            'active': True,
            'builtIn': False,
            'uiUrl': ui_url,
            'url': url,
            'whitelistDomains': domains,
        }
        resp = self.session.post(self._cluster_driver_list_url, json=data)
        assert resp.status_code in [200, 201], f'{resp.status_code} not in [200, 201]'
        LOGGER.debug('Successfully created driver via API: \n%s', resp.json())
        return resp.json()

    def find_cce_driver(self):
        """Returns found OTC CCE driver information or None"""
        resp = self.session.get(self._cluster_driver_list_url,
                                params={'name': CCE_DRIVER_NAME})
        drivers = resp.json()['data']
        if not drivers:
            LOGGER.debug('Found no driver with name %s', CCE_DRIVER_NAME)
            return None
        LOGGER.debug('Found %s drivers with name %s',
                     len(drivers), CCE_DRIVER_NAME)
        return drivers[0]

    def _existing_driver(self):
        end_time = time.monotonic() + 60
        # wait for driver to appear in the driver list
        while time.monotonic() < end_time:
            _drv = self.find_cce_driver()
            if _drv is not None:
                return _drv
        raise TimeoutError(f'CCE driver not existing after '
                           f'${DRIVER_ACTIVATING} seconds')

    def wait_cce_driver_state(self, expected='active'):
        """Wait until driver is activated"""
        _links = self._existing_driver()['links']
        end_time = time.monotonic() + DRIVER_ACTIVATING
        while time.monotonic() < end_time:
            _drv = self.session.get(_links['self']).json()
            if _drv['state'] == expected:
                return
            time.sleep(1)

        raise TimeoutError(f'CCE driver failed to reach `${expected}` '
                           f'state in ${DRIVER_ACTIVATING} seconds')

    def delete_cce_driver(self):
        driver = self.find_cce_driver()
        if driver is None:
            LOGGER.debug('No driver exists, nothing to delete')
            return
        resp = self.session.delete(driver['links']['remove'])
        assert resp.status_code == 200
        self.wait_for_404(driver['links']['self'])
        LOGGER.debug('CCE driver deleted')

    def wait_for_404(self, url, timeout=30):
        end_time = time.monotonic() + timeout
        while time.monotonic() < end_time:
            resp = self.session.get(url)
            if resp.status_code == 404:
                return
        raise TimeoutError(f'Failed get 404 on "{url}"')

    def find_cluster(self, name):
        resp = self.session.get(self._cluster_list_url,
                                params={'driver': CCE_DRIVER_NAME, 'name': name})
        clusters = resp.json()['data']
        if not clusters:
            LOGGER.debug('Found no `%s` cluster with name %s', CCE_DRIVER_NAME, name)
            return None
        LOGGER.debug('Found %s `%s` cluster(s) with name %s',
                     len(clusters), CCE_DRIVER_NAME, name)
        return clusters[0]

    def delete_cluster(self, name):
        cluster = self.find_cluster(name)
        if cluster is None:
            LOGGER.debug('No cluster exists, nothing to delete')
            return
        resp = self.session.delete(cluster['links']['remove'])
        assert resp.status_code == 200
        self.wait_for_404(cluster['links']['self'], timeout=CLUSTER_DELETED)
        LOGGER.debug('CCE cluster deleted')
