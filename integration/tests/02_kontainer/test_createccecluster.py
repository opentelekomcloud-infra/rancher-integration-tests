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

# import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.keys import Keys


class TestCreateccecluster():
    def test_create_cce_cluster(self, rancher_conf, selenium_driver):
        try:
            # Test name: create-cce-cluster
            # Step # | name | target | value
            # 1 | open | /login |
            selenium_driver.get("https://%s:%s/login" % (
                rancher_conf.bind_host, rancher_conf.rancher_port))
            # 2 | setWindowSize | 1552x840 |
            selenium_driver.set_window_size(1552, 840)
            # 3 | type | id=login-username-local | admin
            selenium_driver.find_element(
                By.ID, "login-username-local"
            ).send_keys("admin")
            # 4 | click | id=login-password-local |
            self.element = selenium_driver.find_element(
                By.ID, "login-password-local")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 5 | type | id=login-password-local |
            selenium_driver.find_element(
                By.ID, "login-password-local"
            ).send_keys(rancher_conf.rancher_password)
            # 6 | click | css=.bg-primary |
            self.element = selenium_driver.find_element(
                By.CSS_SELECTOR, ".bg-primary")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 7 | click | xpath=//a[contains(.,'Add Cluster')] |
            self.element = selenium_driver.find_element(
                By.XPATH, "//a[contains(.,\'Add Cluster\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 8 | click |
            #  xpath=//div[contains(@class, 'machine-driver generic otc')] |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//div[contains(@class, \'machine-driver generic otc\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 9 | click | xpath=//div[contains(.,'Cluster Name')]/div/input |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'Cluster Name\')]/div/input")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 10 | type | xpath=//div[contains(.,'Cluster Name')]/div/input |
            selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'Cluster Name\')]/div/input"
            ).send_keys(rancher_conf.cluster_name)
            # 11 | click | name=domain-name |
            self.element = selenium_driver.find_element(
                By.NAME, "domain-name")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 12 | type | name=domain-name |
            selenium_driver.find_element(
                By.NAME, "domain-name"
            ).send_keys(rancher_conf.cce_domain_name)
            # 13 | click | name=project-name |
            self.element = selenium_driver.find_element(
                By.NAME, "project-name")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 14 | type | name=project-name |
            selenium_driver.find_element(
                By.NAME, "project-name"
            ).send_keys(rancher_conf.cce_project_name)
            # 15 | click | name=username |
            self.element = selenium_driver.find_element(
                By.NAME, "username")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 16 | type | name=username |
            selenium_driver.find_element(
                By.NAME, "username"
            ).send_keys(rancher_conf.cce_user_name)
            # 17 | click | name=passsword |
            self.element = selenium_driver.find_element(
                By.NAME, "passsword")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 18 | type | name=passsword |
            selenium_driver.find_element(
                By.NAME, "passsword"
            ).send_keys(rancher_conf.cce_password)
            # 19 | click | css=.bg-primary |
            self.element = selenium_driver.find_element(
                By.CSS_SELECTOR, ".bg-primary")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 20 | click |
            #  xpath=//button[contains(.,'Next: Network configuration')] |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//button[contains(.,\'Next: Network configuration\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 21 | click | xpath=//div
            #  [contains(.,'Virtual Private Cloud')]/span/div/div/input |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'Virtual Private Cloud\')"
                "]/span/div/div/input")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 22 | click | xpath=//div[contains(.,'Virtual Private Cloud')]
            #  /span/div/div/section/div[contains(.,'vpc_name')] |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'Virtual Private Cloud\')]"
                "/span/div/div/section/div["
                "contains(.,\'%s\')]" %
                rancher_conf.vpc_name)
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 23 | click | xpath=//div[contains(.,'Subnet')]i
            #  /span/div/div/input |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'Subnet\')]/span/div/div/input")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 24 | click | xpath=//div[contains(.,'Subnet')]
            #  /span/div/div/section/div[contains(.,'rancher_cce_subnet_name')]
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'Subnet\')]/span/div"
                "/div/section/div[contains(.,\'%s\')]" %
                rancher_conf.subnet_name)
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 25 | click |
            #  xpath=//button[contains(.,'Next: Cluster Floating IP')] |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//button[contains(.,\'Next: Cluster Floating IP\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 26 | runScript | window.scrollTo(0,655.2000122070312) |
            selenium_driver.execute_script(
                "window.scrollTo(0,655.2000122070312)")
            # 27 | click |
            #  xpath=//button[contains(.,'Next: Node Configuration')] |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//button[contains(.,\'Next: Node Configuration\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 28 | click |
            #  xpath=//div[contains(.,'SSH Key Pair')]/span/div/div/input |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'SSH Key Pair\')]"
                "/span/div/div/input")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 29 | click | xpath=//div[contains(.,'SSH Key Pair')]
            #  /span/div/div/section/div
            #  [contains(.,'rancher_cce_keypair_name')] |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'SSH Key Pair\')]"
                "/span/div/div/section/div[contains(.,\'%s\')]" %
                rancher_conf.keypair_name)
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 30 | click |
            #  xpath=//button[contains(.,'Next: Nodes disk configuration')] |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//button[contains(.,\'Next: Nodes disk configuration\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 31 | runScript | window.scrollTo(0,1094.4000244140625) |
            selenium_driver.execute_script(
                "window.scrollTo(0,1094.4000244140625)")
            # 35 | click |
            #  xpath=//button[contains(.,'Finish & Create Cluster')] |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//button[contains(.,\'Finish & Create Cluster\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 36 | assertText | linkText={{ rancher_cce_cluster_name }} |
            assert selenium_driver.find_element(
                By.LINK_TEXT, rancher_conf.cluster_name).text == \
                rancher_conf.cluster_name
            # 37 | assertText | xpath=//tr
            #  [contains(.,'rancher_cce_cluster_name')]
            #  /td/span[contains(.,'Provisioning')] | Provisioning
            assert selenium_driver.find_element(
                By.XPATH,
                "//tr[contains(.,\'%s\')]/td/span"
                "[contains(.,\'Provisioning\')]" %
                rancher_conf.cluster_name).text \
                == "Provisioning"
            # 38 | waitForElementPresent |
            #  xpath=//tr[contains(.,'rancher_cce_cluster_name')]
            #  /td/span[contains(.,'Active')] | 900
            WebDriverWait(
                selenium_driver, 900
            ).until(expected_conditions.presence_of_element_located(
                (By.XPATH,
                 "//tr[contains(.,\'%s\')]/td/span[contains(.,\'Active\')]" %
                 rancher_conf.cluster_name)))
            # 39 | assertText | xpath=//tr
            #  [contains(.,'rancher_cce_cluster_name')]
            #  /td/span[contains(.,'Active')] | Active
            assert selenium_driver.find_element(
                By.XPATH,
                "//tr[contains(.,\'%s\')]/td/span"
                "[contains(.,\'Active\')]" %
                rancher_conf.cluster_name).text \
                == "Active"
            # 40 | click | xpath=//tr
            #  [contains(.,'rancher_cce_cluster_name')]/td/input |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//tr[contains(.,\'%s\')]/td/input" %
                rancher_conf.cluster_name)
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 41 | click | linkText=Delete |
            self.element = selenium_driver.find_element(
                By.LINK_TEXT, "Delete")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 42 | click | xpath=//button[contains(.,'Delete')] |
            self.element = selenium_driver.find_element(
                By.XPATH,
                "//button[contains(.,\'Delete\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 43 | waitForElementPresent |
            #  xpath=//tr[contains(.,'rancher_cce_cluster_name')]
            #  /td/span[contains(.,'Removing')] | 30
            WebDriverWait(
                selenium_driver, 30
            ).until(expected_conditions.presence_of_element_located(
                (By.XPATH,
                 "//tr[contains(.,\'%s\')]/td/span"
                 "[contains(.,\'Removing\')]" %
                 rancher_conf.cluster_name)))
            # 44 | waitForElementNotPresent |
            #  linkText=rancher_cce_cluster_name | 450
            WebDriverWait(
                selenium_driver, 450
            ).until(expected_conditions.invisibility_of_element_located(
                (By.LINK_TEXT,
                 rancher_conf.cluster_name)))
        except Exception as e:
            print(e)
            selenium_driver.save_screenshot("screenshot-exception.png")
            raise
