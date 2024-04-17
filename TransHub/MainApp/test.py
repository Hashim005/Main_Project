
from datetime import datetime
from os import name
from django.forms import Select
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()

        
    def test_01_login_page(self):   
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)


        login = driver.find_element(By.CSS_SELECTOR, "a#login")
        login.click()
        time.sleep(2)
        username = driver.find_element(By.CSS_SELECTOR, "input#username")
        username.send_keys("Hashim")
        password = driver.find_element(By.CSS_SELECTOR, "input#password")
        password.send_keys("H@$h1m")
        time.sleep(1)
        submitc = driver.find_element(By.CSS_SELECTOR, "button#login-btn")
        submitc.click()
        time.sleep(2)

        #trip catagery

        trip_category = driver.find_element(By.CSS_SELECTOR, "a#trip_category")
        trip_category.click()
        time.sleep(2)

        add_category = driver.find_element(By.CSS_SELECTOR, "button#add_new")
        add_category.click()
        time.sleep(2)

        category_name = driver.find_element(By.CSS_SELECTOR, "input#name")
        category_name.send_keys("AC")
        description = driver.find_element(By.CSS_SELECTOR, "textarea#description")
        description.send_keys("Non-stop bus")

        status = driver.find_element(By.CSS_SELECTOR, "select#status")
        status_option = status.find_elements(By.TAG_NAME, 'option')[0]  # Assuming the first option is a placeholder
        status_option.click()

        submit_category = driver.find_element(By.CSS_SELECTOR, "button#submit")
        submit_category.click()
        time.sleep(2)

        driver.back()



        #bus location

        bus_location = driver.find_element(By.CSS_SELECTOR, "a#bus_location")
        bus_location.click()
        time.sleep(2)

        add_location = driver.find_element(By.CSS_SELECTOR, "button#add_new")
        add_location.click()
        time.sleep(2)

        location = driver.find_element(By.CSS_SELECTOR, "textarea#location")
        location.send_keys("Kollam")

        status = driver.find_element(By.CSS_SELECTOR, "select#status")
        status_option = status.find_elements(By.TAG_NAME, 'option')[0]  # Assuming the first option is a placeholder
        status_option.click()

        submit_trip_shedule = driver.find_element(By.CSS_SELECTOR, "button#submit")
        submit_trip_shedule.click()
        time.sleep(2)

        driver.back()

        logout = driver.find_element(By.CSS_SELECTOR, "a#logout")
        logout.click()
        time.sleep(2)

        #login as user

        login = driver.find_element(By.CSS_SELECTOR, "a#login")
        login.click()
        time.sleep(2)
        username = driver.find_element(By.CSS_SELECTOR, "input#username")
        username.send_keys("Nintu")
        password = driver.find_element(By.CSS_SELECTOR, "input#password")
        password.send_keys("Nintu@123")
        time.sleep(1)
        submitc = driver.find_element(By.CSS_SELECTOR, "button#login-btn")
        submitc.click()
        time.sleep(2)

        booknow = driver.find_element(By.CSS_SELECTOR, "a#booknow")
        booknow.click()
        time.sleep(2)

        feedback = driver.find_element(By.CSS_SELECTOR, "a#feedback")
        feedback.click()
        time.sleep(2)

        feedback_form = driver.find_element(By.CSS_SELECTOR, "textarea#feedback_form")
        feedback_form.send_keys("Misbehaviour of driver")

        feedback_submit = driver.find_element(By.CSS_SELECTOR, "button#feedback_submit")
        feedback_submit.click()
        time.sleep(2)

        print("Test sucessfully completed")



if name == 'main':
    import unittest
    unittest.main()