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

import pytest
from pyasli import BrowserSession
from selenium.webdriver import DesiredCapabilities

from integration.tests.pages import (
    CCEClusterConfigPage, ClusterDriversListPage, ClusterListPage, LoginPage,
    NewClusterSelectPage
)


class RancherConfig:
    bind_host: str
    password: str
    rancher_port: str
    selenium_port: str
    rancher_password: str
    kontainer_driver_location: str
    kontainer_driver_ui_location: str
    whitelist: str
    cluster_name: str
    cce_domain_name: str
    cce_project_name: str
    cce_user_name: str
    cce_password: str
    vpc_name: str
    subnet_name: str
    cce_keypair_name: str


@pytest.fixture(scope='session')
def rancher_conf():
    obj = RancherConfig()
    obj.bind_host = os.environ.get('RANCHER_BIND_HOST')
    if not obj.bind_host:
        try:
            obj.bind_host = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            cmd = ("ip route | grep default | sed -En 's/.*(via )"
                   "(([0-9]*\\.){3}[0-9]*).*/\2/p'")
            obj.bind_host = os.popen(cmd).read()
            print('Using %s as bind_host' % obj.bind_host)

    obj.rancher_port = os.environ.get('RANCHER_PORT', '443')
    obj.selenium_port = os.environ.get('SELENIUM_PORT', '4444')
    obj.rancher_password = os.environ.get('RANCHER_PASSWORD')
    obj.kontainer_driver_location = os.environ.get('RANCHER_DRIVER_LOCATION')
    obj.kontainer_driver_ui_location = os.environ.get(
        'RANCHER_DRIVER_UI_LOCATION')
    obj.whitelist = os.environ.get('RANCHER_WHITELIST')
    obj.cluster_name = os.environ.get('RANCHER_CLUSTER_NAME')
    obj.cce_domain_name = os.environ.get('RANCHER_CCE_DOMAIN_NAME')
    obj.cce_project_name = os.environ.get('RANCHER_CCE_PROJECT_NAME')
    obj.cce_user_name = os.environ.get('RANCHER_CCE_USER_NAME')
    obj.cce_password = os.environ.get('RANCHER_CCE_PASSWORD')
    obj.vpc_name = os.environ.get('RANCHER_CCE_VPC_NAME')
    obj.subnet_name = os.environ.get('RANCHER_CCE_SUBNET_NAME')
    obj.keypair_name = os.environ.get('RANCHER_CCE_KEYPAIR_NAME')
    yield obj


@pytest.fixture(scope='module')
def browser(rancher_conf, base_url):
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
        yield instance


@pytest.fixture(scope='session')
def base_url(rancher_conf):
    return f'https://{rancher_conf.bind_host}:{rancher_conf.rancher_port}'


@pytest.fixture
def login_page(browser):
    return LoginPage(browser)


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
