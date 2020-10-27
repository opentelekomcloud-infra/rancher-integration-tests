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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestAddclusterdriver:

    def test_addclusterdriver(self, rancher_conf, selenium_driver):
        try:
            # Test name: add-cluster-driver
            # Step # | name | target | value
            # 1 | open | /login |
            selenium_driver.get(
                "https://%s:%s/n/drivers/cluster" % (
                    rancher_conf.bind_host, rancher_conf.rancher_port))
            # 2 | setWindowSize | 1552x840 |
            selenium_driver.set_window_size(1552, 840)
            # 3 | type | id=login-username-local | admin
            WebDriverWait(
                selenium_driver, 60
            ).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, "login-username-local")))
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
                By.ID,
                "login-password-local"
            ).send_keys(rancher_conf.rancher_password)
            # 6 | click | css=.bg-primary |
            self.element = selenium_driver.find_element(
                By.CSS_SELECTOR, ".bg-primary")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            self.element = selenium_driver.find_element(
                By.CSS_SELECTOR, ".footer-actions > .btn")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 8 | click | xpath=//button[contains(.,'Add Cluster Driver')] |
            self.element = selenium_driver.find_element(
                By.XPATH, "//button[contains(.,\'Add Cluster Driver\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 9 | click | xpath=//div[contains(.,'Download URL')]/input |
            self.element = selenium_driver.find_element(
                By.XPATH, "//div[contains(.,\'Download URL\')]/input")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 10 | type | xpath=//div[contains(.,'Download URL')]/input | URL
            selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'Download URL\')]/input"
            ).send_keys(rancher_conf.kontainer_driver_location)
            # 11 | click | xpath=//div[contains(.,'Custom UI URL')]/input |
            self.element = selenium_driver.find_element(
                By.XPATH, "//div[contains(.,\'Custom UI URL\')]/input")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 12 | type | xpath=//div[contains(.,'Custom UI URL')]/input | URL
            selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'Custom UI URL\')]/input"
            ).send_keys(rancher_conf.kontainer_driver_ui_location)
            # 13 | click | xpath=//span[contains(.,'Add Domain')] |
            self.element = selenium_driver.find_element(
                By.XPATH, "//span[contains(.,\'Add Domain\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 14 | type |
            #  xpath=//div[contains(.,'Whitelist Domains')]/div/span/input |
            #  *.otc.t-systems.com
            selenium_driver.find_element(
                By.XPATH,
                "//div[contains(.,\'Whitelist Domains\')]/div/span/input"
            ).send_keys(rancher_conf.whitelist)
            # 15 | click | xpath=//button[contains(.,'Create')] |
            self.element = selenium_driver.find_element(
                By.XPATH, "//button[contains(.,\'Create\')]")
            ActionChains(selenium_driver).move_to_element(
                self.element).click().perform()
            # 16 | waitForElementPresent |
            #  xpath=//tr[contains(.,'Otc')]/td/span
            #  [contains(.,'Activating')] | 60
            WebDriverWait(selenium_driver, 60).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH,
                     "//tr[contains(.,\'Otc\')]/td/span"
                     "[contains(.,\'Activating\')]")))
            # 17 | waitForElementPresent |
            #  xpath=//tr[contains(.,'Otc')]/td/span[contains(.,'Active')] | 60
            WebDriverWait(selenium_driver, 60).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH,
                     "//tr[contains(.,\'Otc\')]/td/span"
                     "[contains(.,\'Active\')]")))
        except Exception as ex:
            print(ex)
            selenium_driver.save_screenshot("screenshot-exception.png")
            raise
