# # Test 1: Login test

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
        username_input.send_keys('luca@gmail.com')
        password_input.send_keys('luca')
        login_button.send_keys(Keys.RETURN)

        assert 'Admin Dashboard' in driver.page_source


# # Test 2: Viewing doctor profile



from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

class ViewDoctorTest(LiveServerTestCase):

    def setUp(self):
        self.username = 'jennyjohnson00137@gmail.com'
        self.password = 'justin@123'

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
        time.sleep(3)  

        # Step 3: Click on "View Doctors" link/button
        view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'View Doctors')
        view_doctors_button.click()
        time.sleep(3)  

        # Step 4: Click on "Book Now" button
        book_now_button = self.driver.find_element(By.LINK_TEXT, 'VIEW PROFILE')
        book_now_button.click()
        time.sleep(3)  

        # Step 5: Verify if "Proceed" button is present on the booking page
        proceed_button = self.driver.find_element(By.LINK_TEXT, 'BOOK APPOINTMENT')
        self.assertIsNotNone(proceed_button)






# # Test 3: Booking appointment

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class DoctorBookingTest(LiveServerTestCase):

    def setUp(self):
        self.username = 'jennyjohnson00137@gmail.com'
        self.password = 'justin@123'

        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get('http://127.0.0.1:8000/user_login/')
        time.sleep(3)
        username_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.NAME, 'submit')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.send_keys(Keys.RETURN)
        time.sleep(3)  

    def test_doctor_booking(self):
        # Step 1: Login
        self.login()

        # Step 2: Navigate to the patient dashboard
        self.driver.get('http://127.0.0.1:8000/patient_dashboard/')
        time.sleep(3)  

        # Step 3: Click on "View Doctors" link/button
        view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'View Doctors')
        view_doctors_button.click()
        time.sleep(3)  

        # Step 4: Click on "Book Now" button
        book_now_button = self.driver.find_element(By.LINK_TEXT, 'BOOK APPOINTMENT')
        book_now_button.click()
        time.sleep(3)  


       # Step 5: Select slot from the dropdown
        select = Select(self.driver.find_element(By.NAME, 'from_to'))
        select.select_by_index(2)  
        time.sleep(3)

        # Step 6: Click on "Proceed" button
        proceed_button = self.driver.find_element(By.XPATH, '//button[@type="submit" and text()="Proceed"]')
        proceed_button.click()
        time.sleep(3)
        # Step 7: Verify if "Proceed" button is present on the booking page
        proceed_button = self.driver.find_element(By.LINK_TEXT, 'Home')
        self.assertIsNotNone(proceed_button)




# # Test 4: Doctor approving appointment

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class DoctorApprovalTest(LiveServerTestCase):

    def setUp(self):
        self.username = 'alfiyaps2024a@mca.ajce.in'
        self.password = 'adhil@123'

        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get('http://127.0.0.1:8000/user_login/')
        time.sleep(3)
        username_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.NAME, 'submit')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.send_keys(Keys.RETURN)
        time.sleep(3)  

    def test_doctor_booking(self):
        # Step 1: Login
        self.login()

        # Step 2: Navigate to the patient dashboard
        self.driver.get('http://127.0.0.1:8000/doctor_dashboard/')
        time.sleep(3)  

        # Step 3: Click on "View Doctors" link/button
        view_booking = self.driver.find_element(By.XPATH, '//button[@type="submit" and text()="Approve"]')
        view_booking.click()
        time.sleep(3)  

        
        # Step 4: 
        proceed_button = self.driver.find_element(By.LINK_TEXT, 'Reschedule')
        self.assertIsNotNone(proceed_button)




# # Test 5: Doctor adding slot

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class DoctorAddSlotTest(LiveServerTestCase):

    def setUp(self):
        self.username = 'aleenaannshaji2024a@mca.ajce.in'
        self.password = 'albin@123'

        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get('http://127.0.0.1:8000/user_login/')
        time.sleep(3)
        username_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.NAME, 'submit')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.send_keys(Keys.RETURN)
        time.sleep(3)  

    def test_doctor_booking(self):
        # Step 1: Login
        self.login()

        # Step 2: Navigate to the patient dashboard
        self.driver.get('http://127.0.0.1:8000/doctor_dashboard/')
        time.sleep(3)  


        schedule_timings_button = self.driver.find_element(By.LINK_TEXT, 'Schedule Timings')
        schedule_timings_button.click()
        time.sleep(3)

        # Step 6: Fill and submit the form
        date_input = self.driver.find_element(By.ID, 'date')
        date_input.clear()  
        date_input.send_keys('06-05-2024')  

        # Select checkboxes by their IDs
        checkboxes = ['slot1', 'slot2', 'slot3']  
        for checkbox_id in checkboxes:
            checkbox = self.driver.find_element(By.ID, checkbox_id)
            if not checkbox.is_selected():
                checkbox.click()

        # Click on the "Add" button
        add_button = self.driver.find_element(By.XPATH, '//button[@type="submit" and text()="Add"]')
        add_button.click()
        time.sleep(3)

        proceed_button = self.driver.find_element(By.LINK_TEXT, 'Timings')
        self.assertIsNotNone(proceed_button)