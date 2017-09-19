from django.utils import timezone
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from pyvirtualdisplay import Display
from django.test import LiveServerTestCase

from django.test.testcases import LiveServerThread
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from django.contrib.auth.models import User

import os
import base64
import uuid
import string
import random


class AddTestCase(StaticLiveServerTestCase):


	def setUp(self):
		#self.display = Display(visible=0, size=(1000, 1200))
		#self.display.start()
		#d = DesiredCapabilities.CHROME
		#d['loggingPrefs'] = { 'browser':'ALL' }
		#self.selenium = webdriver.Chrome(desired_capabilities=d)
		User.objects.create_superuser(
			username='admin',
			password='admin',
			email='admin@example.com'
		)
		super(AddTestCase, self).setUp()
		self.selenium = webdriver.Chrome()
		self.port = self.live_server_url.split(":")[2]
		#self.test_username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
		#self.test_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


	def tearDown(self):
		self.selenium.quit()
		super(AddTestCase, self).tearDown()
		# self.display.stop()
		return


	def test_a_one(self):
		print("start first test")
		pass
	
	def test_profile_admin(self):
		browser = self.selenium
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("admin")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin")
		browser.find_element_by_name('submitbutton').click()		
		url = self.live_server_url + '/accounts/profile/'
		assert 'Profile Page' in browser.title

	"""
	def test_a_register_reporter(self):
		browser = self.selenium
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("admin")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin")
		browser.find_element_by_name('submitbutton').click()		
		
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"Admin"),
		        "Admin Page"
		    )
		)
	"""
		