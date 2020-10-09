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

class TestCreateccecluster():
  def setup_method(self, method):
    self.capability = DesiredCapabilities.CHROME
    self.capability['acceptInsecureCerts']=True
    self.driver = webdriver.Remote(command_executor='http://%s:4444/wd/hub' %
                                   os.environ.get('RANCHER_BIND_HOST'), desired_capabilities=self.capability)
    self.driver.implicitly_wait(30)
    self.vars = {}

  def teardown_method(self, method):
    self.driver.quit()

  def test_createccecluster(self):
    try:
      # Test name: create-cce-cluster
      # Step # | name | target | value
      # 1 | open | /login |
      self.driver.get("https://%s/login" % os.environ.get('RANCHER_BIND_HOST'))
      # 2 | setWindowSize | 1552x840 |
      self.driver.set_window_size(1552, 840)
      # 3 | type | id=login-username-local | admin
      self.driver.find_element(By.ID, "login-username-local").send_keys("admin")
      # 4 | click | id=login-password-local |
      self.element=self.driver.find_element(By.ID, "login-password-local")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 5 | type | id=login-password-local |
      self.driver.find_element(By.ID, "login-password-local").send_keys(os.environ.get('RANCHER_PASSWORD'))
      # 6 | click | css=.bg-primary |
      self.element=self.driver.find_element(By.CSS_SELECTOR, ".bg-primary")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 7 | click | xpath=//a[contains(.,'Add Cluster')] |
      self.element=self.driver.find_element(By.XPATH, "//a[contains(.,\'Add Cluster\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 8 | click | xpath=//div[contains(@class, 'machine-driver generic otc')] |
      self.element=self.driver.find_element(By.XPATH, "//div[contains(@class, \'machine-driver generic otc\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 9 | click | xpath=//div[contains(.,'Cluster Name')]/div/input |
      self.element=self.driver.find_element(By.XPATH, "//div[contains(.,\'Cluster Name\')]/div/input")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 10 | type | xpath=//div[contains(.,'Cluster Name')]/div/input |
      self.driver.find_element(By.XPATH, "//div[contains(.,\'Cluster Name\')]/div/input").send_keys(os.environ.get('RANCHER_CLUSTER_NAME'))
      # 11 | click | name=domain-name |
      self.element=self.driver.find_element(By.NAME, "domain-name")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 12 | type | name=domain-name |
      self.driver.find_element(By.NAME, "domain-name").send_keys(os.environ.get('RANCHER_CCE_DOMAIN_NAME'))
      # 13 | click | name=project-name |
      self.element=self.driver.find_element(By.NAME, "project-name")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 14 | type | name=project-name |
      self.driver.find_element(By.NAME, "project-name").send_keys(os.environ.get('RANCHER_CCE_PROJECT_NAME'))
      # 15 | click | name=username |
      self.element=self.driver.find_element(By.NAME, "username")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 16 | type | name=username |
      self.driver.find_element(By.NAME, "username").send_keys(os.environ.get('RANCHER_CCE_USER_NAME'))
      # 17 | click | name=passsword |
      self.element=self.driver.find_element(By.NAME, "passsword")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 18 | type | name=passsword |
      self.driver.find_element(By.NAME, "passsword").send_keys(os.environ.get('RANCHER_CCE_PASSWORD'))
      # 19 | click | css=.bg-primary |
      self.element=self.driver.find_element(By.CSS_SELECTOR, ".bg-primary")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 20 | click | xpath=//button[contains(.,'Next: Network configuration')] |
      self.element=self.driver.find_element(By.XPATH, "//button[contains(.,\'Next: Network configuration\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 21 | click | xpath=//div[contains(.,'Virtual Private Cloud')]/span/div/div/input |
      self.element=self.driver.find_element(By.XPATH, "//div[contains(.,\'Virtual Private Cloud\')]/span/div/div/input")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 22 | click | xpath=//div[contains(.,'Virtual Private Cloud')]/span/div/div/section/div[contains(.,'{{ rancher_cce_vpc_name }}')] |
      self.element=self.driver.find_element(By.XPATH, "//div[contains(.,\'Virtual Private Cloud\')]/span/div/div/section/div[contains(.,\'%s\')]" % os.environ.get('RANCHER_VPC_NAME'))
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 23 | click | xpath=//div[contains(.,'Subnet')]/span/div/div/input |
      self.element=self.driver.find_element(By.XPATH, "//div[contains(.,\'Subnet\')]/span/div/div/input")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 24 | click | xpath=//div[contains(.,'Subnet')]/span/div/div/section/div[contains(.,'{{ rancher_cce_subnet_name }}')] |
      self.element=self.driver.find_element(By.XPATH,
                                            "//div[contains(.,\'Subnet\')]/span/div/div/section/div[contains(.,\'%s\')]"
                                            %
                                            os.environ.get('RANCHER_SUBNET_NAME'))
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 25 | click | xpath=//button[contains(.,'Next: Cluster Floating IP')] |
      self.element=self.driver.find_element(By.XPATH, "//button[contains(.,\'Next: Cluster Floating IP\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 26 | runScript | window.scrollTo(0,655.2000122070312) |
      self.driver.execute_script("window.scrollTo(0,655.2000122070312)")
      # 27 | click | xpath=//button[contains(.,'Next: Node Configuration')] |
      self.element=self.driver.find_element(By.XPATH, "//button[contains(.,\'Next: Node Configuration\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 28 | click | xpath=//div[contains(.,'SSH Key Pair')]/span/div/div/input |
      self.element=self.driver.find_element(By.XPATH, "//div[contains(.,\'SSH Key Pair\')]/span/div/div/input")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 29 | click | xpath=//div[contains(.,'SSH Key Pair')]/span/div/div/section/div[contains(.,'{{ rancher_cce_keypair_name }}')] |
      self.element=self.driver.find_element(By.XPATH, "//div[contains(.,\'SSH Key Pair\')]/span/div/div/section/div[contains(.,\'%s\')]" % os.environ.get('RANCHER_KEYPAIR_NAME'))
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 30 | click | xpath=//button[contains(.,'Next: Nodes disk configuration')] |
      self.element=self.driver.find_element(By.XPATH, "//button[contains(.,\'Next: Nodes disk configuration\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 31 | runScript | window.scrollTo(0,1094.4000244140625) |
      self.driver.execute_script("window.scrollTo(0,1094.4000244140625)")
      # 35 | click | xpath=//button[contains(.,'Finish & Create Cluster')] |
      self.element=self.driver.find_element(By.XPATH, "//button[contains(.,\'Finish & Create Cluster\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 36 | assertText | linkText={{ rancher_cce_cluster_name }} |
      assert self.driver.find_element(By.LINK_TEXT, os.environ.get('RANCHER_CLUSTER_NAME')).text == os.environ.get('RANCHER_CLUSTER_NAME')
      # 37 | assertText | xpath=//tr[contains(.,'{{ rancher_cce_cluster_name }}')]/td/span[contains(.,'Provisioning')] | Provisioning
      assert self.driver.find_element(By.XPATH, "//tr[contains(.,\'{{ rancher_cce_cluster_name }}\')]/td/span[contains(.,\'Provisioning\')]").text == "Provisioning"
      # 38 | waitForElementPresent | xpath=//tr[contains(.,'{{ rancher_cce_cluster_name }}')]/td/span[contains(.,'Active')] | 900
      WebDriverWait(self.driver,
                    900).until(expected_conditions.presence_of_element_located((By.XPATH,
                                                                                "//tr[contains(.,\'%s\')]/td/span[contains(.,\'Active\')]"
                                                                               %
                                                                               os.environ.get('RANCHER_CLUSTER_NAME'))))
      # 39 | assertText | xpath=//tr[contains(.,'{{ rancher_cce_cluster_name }}')]/td/span[contains(.,'Active')] | Active
      assert self.driver.find_element(By.XPATH, "//tr[contains(.,\'{{ rancher_cce_cluster_name }}\')]/td/span[contains(.,\'Active\')]").text == "Active"
      # 40 | click | xpath=//tr[contains(.,'{{ rancher_cce_cluster_name }}')]/td/input |
      self.element=self.driver.find_element(By.XPATH, "//tr[contains(.,\'{{ rancher_cce_cluster_name }}\')]/td/input")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 41 | click | linkText=Delete |
      self.element=self.driver.find_element(By.LINK_TEXT, "Delete")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 42 | click | xpath=//button[contains(.,'Delete')] |
      self.element=self.driver.find_element(By.XPATH, "//button[contains(.,\'Delete\')]")
      ActionChains(self.driver).move_to_element(self.element).click().perform()
      # 43 | waitForElementPresent | xpath=//tr[contains(.,'{{ rancher_cce_cluster_name }}')]/td/span[contains(.,'Removing')] | 30
      WebDriverWait(self.driver,
                    30).until(expected_conditions.presence_of_element_located((By.XPATH,
                                                                               "//tr[contains(.,\'%s\')]/td/span[contains(.,\'Removing\')]"
                                                                              %
                                                                              os.environ.get('RANCHER_CLUSTER_NAME'))))
      # 44 | waitForElementNotPresent | linkText={{ rancher_cce_cluster_name }} | 450
      WebDriverWait(self.driver, 450).until(expected_conditions.invisibility_of_element_located((By.LINK_TEXT, os.environ.get('RANCHER_CLUSTER_NAME'))))
    except Exception as e:
      print(e)
      self.driver.save_screenshot("screenshot-exception.png")
      raise
