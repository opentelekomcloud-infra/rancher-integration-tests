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
import pytest

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class RancherConfig:
    pass


@pytest.fixture
def rancher_conf():
    obj = RancherConfig()
    obj.password = 'abc'
    obj.bind_host = os.environ.get('RANCHER_BIND_HOST')

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
    obj.cce_keypair_name = os.environ.get('RANCHER_CCE_KEYPAIR_NAME')
    yield obj


@pytest.fixture
def selenium_driver(rancher_conf):
    capability = DesiredCapabilities.CHROME
    capability['acceptInsecureCerts'] = True
    driver = webdriver.Remote(
        command_executor='http://%s:%s/wd/hub' % (
            rancher_conf.bind_host, rancher_conf.selenium_port),
        desired_capabilities=capability)
    driver.implicitly_wait(30)
    yield driver
    driver.quit()
