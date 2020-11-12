import logging

import wrapt
from pyasli import wait_for
from pyasli.bys import by_css, by_id, by_xpath
from pyasli.conditions import enabled, hidden, missing, visible

from integration.tests.helpers.base import Page, field, on_page
from integration.tests.helpers.fields import (
    button, cluster_driver_row, cluster_row, search_select, text_input
)

LOGGER = logging.getLogger('helpers.pages')


def requires_not_existing(locator, timeout=10):
    """Run method only after required element becomes visible"""

    @wrapt.decorator
    def _not_existing(wrapped, instance=None, args=None, kwargs=None):
        if not isinstance(instance, Page):
            raise ValueError('`not_existing` is only applicable to Page fields')
        instance.browser.element(locator).assure(lambda e: not e.exists, timeout)
        return wrapped(*args, **kwargs)

    return _not_existing


class LoginPage(Page):
    url = '/login'

    _username = text_input(by_id('login-username-local'))
    _password = text_input(by_id('login-password-local'))
    _sign_in = button(by_css('button.bg-primary'))

    _modal_ok = button(by_css('div.footer-actions .btn'))

    def login(self, next_url, username, password):
        """Login user and open URL

        :param str next_url: Target page url
        :param str username: Rancher user name
        :param str password: Rancher password
        """
        LOGGER.info('Start logging in')
        self._base.open(next_url)
        self._username.input(username)
        self._password.input(password)
        self._sign_in.click()

        # there can be optional information popup
        self._close_optional_modal()

    def __modal_shown(self):
        try:
            wait_for(self._modal_ok, visible, 5)
            LOGGER.info('First-time modal is shown')
            return True
        except TimeoutError:
            LOGGER.info('First-time modal is NOT shown')
            return False

    def _close_optional_modal(self):
        if not self.__modal_shown():
            return
        self._modal_ok.click()
        self._modal_ok.assure(hidden)


class ClusterDriversListPage(Page):
    url = '/n/drivers/cluster'

    _add_driver = button(by_xpath(r"//button[contains(., 'Add Cluster Driver')]"))

    @on_page
    def click_add_cluster_driver(self):
        self._add_driver.click()

    # register dialog

    _download_url = text_input(by_xpath(r"//div[contains(., 'Download URL')]/input"))
    _custom_ui_url = text_input(by_xpath(r"//div[contains(., 'Custom UI URL')]/input"))
    _add_domain = button(by_xpath(r"//span[contains(., 'Add Domain')]"))
    _domain = text_input(by_xpath(r"//span[@data-title='Whitelist Domains']/input"))
    _create = button(by_xpath(r"//button[contains(., 'Create')]"))

    _modal_window = field('form.modal-container.large-modal')

    def register_driver(self, url, ui_url, allowed_domain=''):
        """Register new cluster driver"""
        LOGGER.info('Start cluster driver registration')
        self._modal_window.assure(visible)
        self._download_url.input(url)
        self._custom_ui_url.input(ui_url)
        if allowed_domain:
            LOGGER.debug('Allowed domain: %s', allowed_domain)
            self._add_domain.click()
            self._domain.input(allowed_domain)
        self._create.click()
        self._modal_window.assure(missing)

    driver_row = cluster_driver_row('kontainer-engine-driver-otccce')


class ClusterListPage(Page):
    url = '/g/clusters'

    _new_cluster_button = button(r'.btn[href="/g/clusters/add"]')

    def click_new_cluster(self):
        self._new_cluster_button.click()

    _delete_button = button(by_xpath(r'//span[contains(text(), "Delete")]'))
    _delete_confirm_button = button('div.footer-actions .bg-error')

    def cluster_row(self, name):
        return cluster_row(name, self)

    def delete(self, name):
        LOGGER.info('Start cluster driver removal')
        self.cluster_row(name).more_actions.click()
        self._delete_button.click()
        self._delete_confirm_button.click()


class NewClusterSelectPage(Page):
    url = '/g/clusters/add/select'

    _otc_cce_button = button(r'div.machine-driver.otccce')

    def click_new_cce_cluster(self):
        self._otc_cce_button.click()


class CCEClusterConfigPage(Page):
    url = '/g/clusters/add/launch/otccce'

    # general
    _name = text_input(r'input[id$="-form-name"]')

    def set_name(self, text):
        self._name.input(text)

    _save = button(r'button[type=submit]')

    def next(self):
        LOGGER.info('Click "Next"')
        self._save.should_be(enabled)
        self._save.click()

    _cancel = button(by_xpath(r'//button[contains(., "Cancel")]'))

    _errors = field(r'div.banner.bg-error')

    def cancel(self):
        self._cancel.click()

    # credentials
    _domain_name = text_input(r'input.ember-text-field[name=domain-name]')
    _project_name = text_input(r'input.ember-text-field[name=project-name]')
    _username = text_input(r'input.ember-text-field[name=username]')
    _password = text_input(r'input.ember-text-field[name=passsword]')

    def input_credentials(self, domain, username, password, project):
        LOGGER.info('Input OTC credentials')
        self._domain_name.input(domain)
        self._username.input(username)
        self._password.input(password)
        self._project_name.input(project)

    # network configuration
    _vpcs = search_select(by_xpath(
        r'//label[contains(text(), "Virtual Private Cloud")]/..'
    ))

    def select_vpc(self, name):
        LOGGER.info('Select VPC')
        self._vpcs.select(name, 0)

    _subnets = search_select(by_xpath(r'//label[text()="Subnet"]/..'))

    def select_subnet(self, name):
        LOGGER.info('Select subnet')
        self._subnets.select(name)

    # node configuration
    _ssh_keys = search_select(by_xpath(r'//label[contains(text(), "SSH Key Pair")]/..'))

    def select_key_pair(self, name):
        LOGGER.info('Select key pair')
        self._ssh_keys.select(name)
