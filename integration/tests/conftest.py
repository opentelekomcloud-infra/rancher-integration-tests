# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import os
import socket
import time
from urllib.parse import urlparse

import pytest
import requests
from pyasli import BrowserSession
from selenium.webdriver import DesiredCapabilities

from integration.tests.helpers.api_client import APIClient
from integration.tests.helpers.pages import (
    CCEClusterConfigPage, ClusterDriversListPage,
    ClusterListPage, LoginPage, NewClusterSelectPage
)


class RancherConfig:
    bind_host: str
    password: str
    rancher_port: str
    selenium_port: str
    rancher_password: str
    kontainer_driver_location: str
    kontainer_driver_ui_location: str
    whitelist: list
    cluster_name: str
    cce_domain_name: str
    cce_project_name: str
    cce_user_name: str
    cce_password: str
    vpc_name: str
    subnet_name: str
    keypair_name: str


@pytest.fixture(scope='session')
def rancher_conf():
    cfg = RancherConfig()
    cfg.bind_host = os.environ.get('RANCHER_BIND_HOST')
    if not cfg.bind_host:
        try:
            cfg.bind_host = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            cmd = ("ip route | grep default | sed -En 's/.*(via )"
                   "(([0-9]*\\.){3}[0-9]*).*/\2/p'")
            cfg.bind_host = os.popen(cmd).read()
            print('Using %s as bind_host' % cfg.bind_host)

    cfg.rancher_port = os.environ.get('RANCHER_PORT', '443')
    cfg.selenium_port = os.environ.get('SELENIUM_PORT', '4444')
    cfg.rancher_password = os.environ.get('RANCHER_PASSWORD')
    cfg.kontainer_driver_location = os.environ.get('RANCHER_DRIVER_LOCATION')
    cfg.kontainer_driver_ui_location = os.environ.get(
        'RANCHER_DRIVER_UI_LOCATION')
    cfg.whitelist = os.environ.get('RANCHER_WHITELIST').split(',')
    # add UI location host to whitelist
    ui_host = urlparse(cfg.kontainer_driver_ui_location).hostname
    if ui_host not in cfg.whitelist:
        cfg.whitelist.append(ui_host)

    cfg.cluster_name = os.environ.get('RANCHER_CLUSTER_NAME')
    cfg.cce_domain_name = os.environ.get('RANCHER_CCE_DOMAIN_NAME')
    cfg.cce_project_name = os.environ.get('RANCHER_CCE_PROJECT_NAME')
    cfg.cce_user_name = os.environ.get('RANCHER_CCE_USER_NAME')
    cfg.cce_password = os.environ.get('RANCHER_CCE_PASSWORD')
    cfg.vpc_name = os.environ.get('RANCHER_CCE_VPC_NAME')
    cfg.subnet_name = os.environ.get('RANCHER_CCE_SUBNET_NAME')
    cfg.keypair_name = os.environ.get('RANCHER_CCE_KEYPAIR_NAME')
    return cfg


@pytest.fixture(scope='session')
def server_is_up(rancher_conf):
    session = requests.session()
    session.verify = False
    end_time = time.monotonic() + 20

    url = f'https://{rancher_conf.bind_host}:{rancher_conf.rancher_port}'
    while time.monotonic() < end_time:
        try:
            resp = session.head(url)
            time.sleep(1)
        except requests.ConnectionError:
            continue
        if resp.status_code == 200:
            return
    raise TimeoutError('Server is not up and running after given timeout')


@pytest.fixture(scope='session')
def browser(rancher_conf, base_url, server_is_up):
    instance = BrowserSession(base_url=base_url)
    capability = DesiredCapabilities.CHROME.copy()
    capability['acceptInsecureCerts'] = True
    with instance:
        instance.setup_browser(
            'chrome',
            remote=True,
            headless=False,
            command_executor='http://{}:{}/wd/hub'.format(
                rancher_conf.bind_host, rancher_conf.selenium_port
            ),
            desired_capabilities=capability,
        )
        instance.open('')
        instance.get_actual().implicitly_wait(0.2)
        instance.get_actual().set_page_load_timeout(30)
        instance.get_actual().set_window_size(1600, 900)
        yield instance


@pytest.fixture(scope='session')
def base_url(rancher_conf):
    return f'https://{rancher_conf.bind_host}:{rancher_conf.rancher_port}'


@pytest.fixture
def cluster_driver_list(browser):
    return ClusterDriversListPage(browser)


@pytest.fixture
def cluster_list(browser):
    return ClusterListPage(browser)


@pytest.fixture
def new_cluster_select(browser):
    return NewClusterSelectPage(browser)


@pytest.fixture
def cluster_config(browser):
    return CCEClusterConfigPage(browser)


@pytest.fixture(scope='session')
def signed_in(browser, rancher_conf):
    login_page = LoginPage(browser)
    # login as admin
    login_page.login('', 'admin', rancher_conf.rancher_password)
    return browser


@pytest.fixture(scope='session')
def api_client(signed_in):
    """HTTP client

    Cookies inherited from browser session
    """
    return APIClient.from_browser_session(signed_in)


@pytest.fixture(scope='session')
def cleanup_cluster_driver(api_client):
    yield
    api_client.delete_cce_driver()


@pytest.fixture(scope='session')
def assure_cluster_driver(api_client, rancher_conf):
    """Create cluster driver if it is missing"""
    existing = api_client.find_cce_driver()
    if existing is not None:
        return
    api_client.create_cluster_driver(
        rancher_conf.kontainer_driver_location,
        rancher_conf.kontainer_driver_ui_location,
        rancher_conf.whitelist,
    )


@pytest.fixture()
def cleanup_cluster(api_client, rancher_conf):
    yield
    api_client.delete_cluster(rancher_conf.cluster_name)
