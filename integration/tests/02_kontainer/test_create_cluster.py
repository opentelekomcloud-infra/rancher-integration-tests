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

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def test_create_cce_cluster(self, rancher_conf, login_page, cluster_list,
                            new_cluster_select, cluster_config):
    # login as admin
    login_page.login(cluster_list.url, 'admin', rancher_conf.rancher_password)

    # open creation page
    cluster_list.click_new_cluster()

    # select OTC CCE
    new_cluster_select.click_new_cce_cluster()

    # setup new cluster

    # login in OTC
    cluster_config.otc_login(
        rancher_conf.cce_domain_name,
        rancher_conf.cce_user_name,
        rancher_conf.cce_password,
        rancher_conf.cce_project_name,
    )

    # use default cluster configuration
    cluster_config.next()

    # select required VPC
    cluster_config.select_vpc(rancher_conf.vpc_name)
    # select required Subnet
    cluster_config.select_subnet(rancher_conf.subnet_name)

    cluster_config.next()

    # 25 | click |
    #  xpath=//button[contains(.,'Next: Cluster Floating IP')] |
    self.element = browser.find_element(
        By.XPATH,
        "//button[contains(.,\'Next: Cluster Floating IP\')]")
    ActionChains(browser).move_to_element(
        self.element).click().perform()
    # 26 | runScript | window.scrollTo(0,655.2000122070312) |
    browser.execute_script(
        "window.scrollTo(0,655.2000122070312)")
    # 27 | click |
    #  xpath=//button[contains(.,'Next: Node Configuration')] |
    self.element = browser.find_element(
        By.XPATH,
        "//button[contains(.,\'Next: Node Configuration\')]")
    ActionChains(browser).move_to_element(
        self.element).click().perform()
    # 28 | click |
    #  xpath=//div[contains(.,'SSH Key Pair')]/span/div/div/input |
    self.element = browser.find_element(
        By.XPATH,
        "//div[contains(.,\'SSH Key Pair\')]"
        "/span/div/div/input")
    ActionChains(browser).move_to_element(
        self.element).click().perform()
    # 29 | click | xpath=//div[contains(.,'SSH Key Pair')]
    #  /span/div/div/section/div
    #  [contains(.,'rancher_cce_keypair_name')] |
    self.element = browser.find_element(
        By.XPATH,
        "//div[contains(.,\'SSH Key Pair\')]"
        "/span/div/div/section/div[contains(.,\'%s\')]" %
        rancher_conf.keypair_name)
    ActionChains(browser).move_to_element(
        self.element).click().perform()
    # 30 | click |
    #  xpath=//button[contains(.,'Next: Nodes disk configuration')] |
    self.element = browser.find_element(
        By.XPATH,
        "//button[contains(.,\'Next: Nodes disk configuration\')]")
    ActionChains(browser).move_to_element(
        self.element).click().perform()
    # 31 | runScript | window.scrollTo(0,1094.4000244140625) |
    browser.execute_script(
        "window.scrollTo(0,1094.4000244140625)")
    # 35 | click |
    #  xpath=//button[contains(.,'Finish & Create Cluster')] |
    self.element = browser.find_element(
        By.XPATH,
        "//button[contains(.,\'Finish & Create Cluster\')]")
    ActionChains(browser).move_to_element(
        self.element).click().perform()
    # 36 | assertText | linkText={{ rancher_cce_cluster_name }} |
    assert browser.find_element(
        By.LINK_TEXT, rancher_conf.cluster_name).text == \
           rancher_conf.cluster_name
    # 37 | assertText | xpath=//tr
    #  [contains(.,'rancher_cce_cluster_name')]
    #  /td/span[contains(.,'Provisioning')] | Provisioning
    assert browser.find_element(
        By.XPATH,
        "//tr[contains(.,\'%s\')]/td/span"
        "[contains(.,\'Provisioning\')]" %
        rancher_conf.cluster_name).text \
           == "Provisioning"
    # 38 | waitForElementPresent |
    #  xpath=//tr[contains(.,'rancher_cce_cluster_name')]
    #  /td/span[contains(.,'Active')] | 900
    WebDriverWait(
        browser, 900
    ).until(expected_conditions.presence_of_element_located(
        (By.XPATH,
         "//tr[contains(.,\'%s\')]/td/span[contains(.,\'Active\')]" %
         rancher_conf.cluster_name)))
    # 39 | assertText | xpath=//tr
    #  [contains(.,'rancher_cce_cluster_name')]
    #  /td/span[contains(.,'Active')] | Active
    assert browser.find_element(
        By.XPATH,
        "//tr[contains(.,\'%s\')]/td/span"
        "[contains(.,\'Active\')]" %
        rancher_conf.cluster_name).text \
           == "Active"
    # 40 | click | xpath=//tr
    #  [contains(.,'rancher_cce_cluster_name')]/td/input |
    self.element = browser.find_element(
        By.XPATH,
        "//tr[contains(.,\'%s\')]/td/input" %
        rancher_conf.cluster_name)
    ActionChains(browser).move_to_element(
        self.element).click().perform()
    # 41 | click | linkText=Delete |
    self.element = browser.find_element(
        By.LINK_TEXT, "Delete")
    ActionChains(browser).move_to_element(
        self.element).click().perform()
    # 42 | click | xpath=//button[contains(.,'Delete')] |
    self.element = browser.find_element(
        By.XPATH,
        "//button[contains(.,\'Delete\')]")
    ActionChains(browser).move_to_element(
        self.element).click().perform()
    # 43 | waitForElementPresent |
    #  xpath=//tr[contains(.,'rancher_cce_cluster_name')]
    #  /td/span[contains(.,'Removing')] | 30
    WebDriverWait(
        browser, 30
    ).until(expected_conditions.presence_of_element_located(
        (By.XPATH,
         "//tr[contains(.,\'%s\')]/td/span"
         "[contains(.,\'Removing\')]" %
         rancher_conf.cluster_name)))
    # 44 | waitForElementNotPresent |
    #  linkText=rancher_cce_cluster_name | 450
    WebDriverWait(
        browser, 450
    ).until(expected_conditions.invisibility_of_element_located(
        (By.LINK_TEXT,
         rancher_conf.cluster_name)))
