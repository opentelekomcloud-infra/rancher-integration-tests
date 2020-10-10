# Generated by Selenium IDE
import pytest
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

class TestAddclusterdriver():
  def setup_method(self, method):
    self.capability = DesiredCapabilities.CHROME
    self.capability['acceptInsecureCerts']=True
    self.driver = webdriver.Remote(command_executor='http://%s:4444/wd/hub' %
                                   os.environ.get('RANCHER_BIND_HOST'), desired_capabilities=self.capability)
    self.driver.implicitly_wait(30)
    self.vars = {}

  def teardown_method(self, method):
    self.driver.quit()

  def test_addclusterdriver(self):
    try:
      # Test name: add-cluster-driver
      # Step # | name | target | value
      # 1 | open | /login |
      self.driver.get("https://%s:8443/n/drivers/cluster" % os.environ.get('RANCHER_BIND_HOST'))
      # 2 | setWindowSize | 1552x840 |
      self.driver.set_window_size(1552, 840)
      # 3 | type | id=login-username-local | admin
      WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located((By.ID, "login-username-local")))
      self.driver.find_element(By.ID, "login-username-local").send_keys("admin")
      # 4 | click | id=login-password-local |
      self.element=self.driver.find_element(By.ID, "login-password-local")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 5 | type | id=login-password-local |
      self.driver.find_element(By.ID, "login-password-local").send_keys(os.environ.get('RANCHER_PASSWORD'))
      # 6 | click | css=.bg-primary |
      self.element=self.driver.find_element(By.CSS_SELECTOR, ".bg-primary")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      self.element= self.driver.find_element(By.CSS_SELECTOR, ".footer-actions > .btn")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 8 | click | xpath=//button[contains(.,'Add Cluster Driver')] |
      self.element=self.driver.find_element(By.XPATH, "//button[contains(.,\'Add Cluster Driver\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 9 | click | xpath=//div[contains(.,'Download URL')]/input |
      self.element=self.driver.find_element(By.XPATH, "//div[contains(.,\'Download URL\')]/input")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 10 | type | xpath=//div[contains(.,'Download URL')]/input | https://github.com/opentelekomcloud/kontainer-engine-driver-otc/releases/download/v0.2.1/kontainer-engine-driver-otc-0.2.1-linux-amd64.tgz
      self.driver.find_element(By.XPATH, "//div[contains(.,\'Download URL\')]/input").send_keys(os.environ.get('RANCHER_DRIVER_LOCATION'))
      # 11 | click | xpath=//div[contains(.,'Custom UI URL')]/input |
      self.element=self.driver.find_element(By.XPATH, "//div[contains(.,\'Custom UI URL\')]/input")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 12 | type | xpath=//div[contains(.,'Custom UI URL')]/input | https://csm-assets.obs.eu-de.otc.t-systems.com/ui/component.js
      self.driver.find_element(By.XPATH, "//div[contains(.,\'Custom UI URL\')]/input").send_keys(os.environ.get('RANCHER_UI_LOCATION'))
      # 13 | click | xpath=//span[contains(.,'Add Domain')] |
      self.element=self.driver.find_element(By.XPATH, "//span[contains(.,\'Add Domain\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 14 | type | xpath=//div[contains(.,'Whitelist Domains')]/div/span/input | *.otc.t-systems.com
      self.driver.find_element(By.XPATH, "//div[contains(.,\'Whitelist Domains\')]/div/span/input").send_keys(os.environ.get('RANCHER_WHITELIST'))
      # 15 | click | xpath=//button[contains(.,'Create')] |
      self.element=self.driver.find_element(By.XPATH, "//button[contains(.,\'Create\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 16 | waitForElementPresent | xpath=//tr[contains(.,'Otc')]/td/span[contains(.,'Activating')] | 60
      WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, "//tr[contains(.,\'Otc\')]/td/span[contains(.,\'Activating\')]")))
      # 17 | waitForElementPresent | xpath=//tr[contains(.,'Otc')]/td/span[contains(.,'Active')] | 60
      WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, "//tr[contains(.,\'Otc\')]/td/span[contains(.,\'Active\')]")))
    except Exception as e:
      print(e)
      self.driver.save_screenshot("screenshot-exception.png")
      raise

