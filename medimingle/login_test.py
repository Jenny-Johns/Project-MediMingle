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























# TEST 1

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



# TEST 2


from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

class DoctorBookingTest(LiveServerTestCase):

    def setUp(self):
        self.username = 'jennyjohnson00137@gmail.com'
        self.password = 'luca@123'

        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get('http://127.0.0.1:8000/user_login/')
        time.sleep(5)
        username_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.NAME, 'submit')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.send_keys(Keys.RETURN)
        time.sleep(5)  

    def test_doctor_booking(self):
        # Step 1: Login
        self.login()

        # Step 2: Navigate to the patient dashboard
        self.driver.get('http://127.0.0.1:8000/patient_dashboard/')
        time.sleep(5)  

        # Step 3: Click on "View Doctors" link/button
        view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'View Doctors')
        view_doctors_button.click()
        time.sleep(5)  

        # Step 4: Click on "Book Now" button
        book_now_button = self.driver.find_element(By.LINK_TEXT, 'BOOK APPOINTMENT')
        book_now_button.click()
        time.sleep(5)  

        # Step 5: Verify if "Proceed" button is present on the booking page
        proceed_button = self.driver.find_element(By.NAME, 'proceed')
        self.assertIsNotNone(proceed_button)


# # TEST 3


from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

class DoctorBookingTest(LiveServerTestCase):

    def setUp(self):
        self.username = 'jennyjohnson00137@gmail.com'
        self.password = 'luca@123'

        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get('http://127.0.0.1:8000/user_login/')
        time.sleep(5)
        username_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.NAME, 'submit')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.send_keys(Keys.RETURN)
        time.sleep(5)  

    def test_doctor_booking(self):
        # Step 1: Login
        self.login()

        # Step 2: Navigate to the patient dashboard
        self.driver.get('http://127.0.0.1:8000/patient_dashboard/')
        time.sleep(5)  

        # Step 3: Click on "Home" link/button
        view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'Home')
        view_doctors_button.click()
        time.sleep(5)  

        # Step 4: Click on "View" button
        book_now_button = self.driver.find_element(By.LINK_TEXT, 'View Profile')
        book_now_button.click()
        time.sleep(5)  

        # Step 5: Verify if "Home" button is present on the page
        proceed_button = self.driver.find_element(By.LINK_TEXT, 'Home')
        self.assertIsNotNone(proceed_button)


# TEST 4


from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

class DoctorBookingTest(LiveServerTestCase):

    def setUp(self):
        self.username = 'luca@gmail.com'
        self.password = 'luca@123'

        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get('http://127.0.0.1:8000/user_login/')
        time.sleep(5)
        username_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.NAME, 'submit')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.send_keys(Keys.RETURN)
        time.sleep(5)  

    def test_doctor_booking(self):
        # Step 1: Login
        self.login()

        # Step 2: Navigate to the admin dashboard
        self.driver.get('http://127.0.0.1:8000/adminpage/')
        time.sleep(5)  

        # Step 3: Click on "Doctors" button
        view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'Doctors')
        view_doctors_button.click()
        time.sleep(5)  
        # Step 4: Click on "View" button to view doctor profile
        book_now_button = self.driver.find_element(By.LINK_TEXT, 'View')
        book_now_button.click()
        time.sleep(5)  

        # Step 5: Verify if "Back to Doctor List" button is present on the page
        button = self.driver.find_element(By.LINK_TEXT, 'Back to Doctor List')
        self.assertIsNotNone(button)
