import unittest
from django.test import TestCase,Client
from selenium.webdriver import Chrome, ChromeOptions
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

# Create your tests here.
class LoginTest(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('lam123')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('123456')
        self.selenium.find_element(By.XPATH, '/input[@value="Log in"]').click()


