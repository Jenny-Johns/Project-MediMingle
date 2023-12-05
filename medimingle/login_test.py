from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Set the path to your ChromeDriver executable
chrome_driver_path = r'C:\Users\user\Desktop\MediMingle\chromedriver.exe'

# Set up the Chrome service
chrome_service = Service(chrome_driver_path)

# Initialize the Chrome browser with the service
driver = webdriver.Chrome(service=chrome_service)

driver.implicitly_wait(10)


# Open the login page
driver.get('http://127.0.0.1:8000/user_login/')

# Find login elements and perform actions
username_input = driver.find_element(By.NAME, 'email')
password_input = driver.find_element(By.NAME, 'password')
login_button = driver.find_element(By.NAME, 'submit')

username_input.send_keys('luca@gmail.com')
password_input.send_keys('luca@123')
login_button.click()

# Add assertions or other validation as needed
assert 'luca' in driver.page_source

# Close the browser
driver.quit()








# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time


# class LoginformTest(LiveServerTestCase):

#     def testloginpage(self):
#         driver = webdriver.Chrome()

#         driver.get('http://127.0.0.1:8000/user_login/')
#         time.sleep(5)
#         email=driver.find_element_by_name('email')
#         password=driver.find_element_by_name('password')
#         time.time(5)
#         submit=driver.find_element_by_name('submit')
#         email.send_keys('jennyjohnson0013@gmail.com')
#         password.send_keys('jenny@123')
#         submit.send_keys(Keys.RETURN)

#         assert 'luca' in driver.page_source

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By

# # Set the path to your ChromeDriver executable
# chrome_driver_path = r'C:\Users\user\Desktop\MediMingle\chromedriver.exe'

# # Set up the Chrome service
# chrome_service = Service(chrome_driver_path)

# # Initialize the Chrome browser with the service
# driver = webdriver.Chrome(service=chrome_service)

# driver.implicitly_wait(10)


# # Open the login page
# driver.get('http://127.0.0.1:8000/user_login/')

# # Find login elements and perform actions
# username_input = driver.find_element(By.NAME, 'email')
# password_input = driver.find_element(By.NAME, 'password')
# login_button = driver.find_element(By.NAME, 'submit')

# username_input.send_keys('luca@gmail.com')
# password_input.send_keys('luca@123')
# login_button.click()

# # Add assertions or other validation as needed
# assert 'luca' in driver.page_source

# # Close the browser
# driver.quit()



