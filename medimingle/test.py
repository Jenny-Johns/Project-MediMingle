
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

class LoginformTest(LiveServerTestCase):

    def testloginpage(self):
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/user_login/')
        time.sleep(5)
        username_input = driver.find_element(By.NAME, 'email')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
        username_input.send_keys('jennyjohnson0013@gmail.com')
        password_input.send_keys('jenny@123')
        login_button.send_keys(Keys.RETURN)

        assert 'jennyjohnson0013@gmail.com' in driver.page_source
