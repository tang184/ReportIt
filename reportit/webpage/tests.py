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

	""" bad page """
	def test_notlogin_dashboard(self):
		browser = self.selenium
		url = self.live_server_url + '/account/dashboard/'
		browser.get(url)
		assert 'You have successfully logged in' not in browser.page_source
	
	""" login """

	def test_adminlogin_profile(self):
		browser = self.selenium
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("admin")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin")
		browser.find_element_by_name('login-submit').click()	
		assert 'You have successfully logged in' in browser.page_source

	def test_adminlogin_wrongpassword(self):
		browser = self.selenium
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("admin")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin1")
		browser.find_element_by_name('login-submit').click()		
		assert 'You have successfully logged in' not in browser.title
		assert 'username' in browser.page_source

	def test_adminlogin_notexist(self):
		browser = self.selenium
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("admin999")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin")
		browser.find_element_by_name('login-submit').click()		
		assert 'You have successfully logged in' not in browser.title
		assert 'username' in browser.page_source

	""" reporter signup """
	def test_reportersignup_good(self):
		browser = self.selenium
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("user")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()		
		assert 'Reporter Signup' not in browser.title

	def test_reportersignup_invalidusername(self):
		browser = self.selenium
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("您好！")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()
		assert 'Reporter Signup' in browser.title
		
	
	def test_reportersignup_invalidemail(self):
		browser = self.selenium
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qqcom')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()		
		assert 'Reporter Signup' in browser.title
		assert 'Enter a valid email address.' in browser.page_source
	
	def test_reportersignup_dismatchpswd(self):
		browser = self.selenium
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass123")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()	
		assert 'The two password fields didn\'t match.'	in browser.page_source	
		assert 'Reporter Signup' in browser.title

	def test_reportersignup_dupuser(self):
		browser = self.selenium
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("admin")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass123")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()
		assert 'A user with that username already exists.' in browser.page_source	
		assert 'Reporter Signup' in browser.title
	

	"""agent signup""" """
	def test_agentsignup_invalidusername(self):
		browser = self.selenium
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("您好！")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		logo = browser.find_element_by_name('agentimage')
		# yet to test
		vfile = browser.find_element_by_name('agentverifile')
		# yet to test
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()		
		assert 'ReportIt Agent Signup' in browser.title

	def test_agentsignup_invalidemail(self):
		browser = self.selenium
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123abc.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		logo = browser.find_element_by_name('agentimage')
		# yet to test
		vfile = browser.find_element_by_name('agentverifile')
		# yet to test
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()		
		assert 'ReportIt Agent Signup' in browser.title

	def test_agentsignup_dismatchpswd(self):
		browser = self.selenium
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@abc.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		logo = browser.find_element_by_name('agentimage')
		# yet to test
		vfile = browser.find_element_by_name('agentverifile')
		# yet to test
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()	
		assert 'The two password fields didn\'t match.'	in browser.page_source
		assert 'ReportIt Agent Signup' in browser.title

	def test_agentsignup_dupuser(self):
		browser = self.selenium
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("admin")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		logo = browser.find_element_by_name('agentimage')
		# yet to test
		vfile = browser.find_element_by_name('agentverifile')
		# yet to test
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()
		assert 'A user with that username already exists.' in browser.page_source
		assert 'ReportIt Agent Signup' in browser.title


	""" """submit concerns""" """

	def test_concern_good(self):
		browser = self.selenium
		url = self.live_server_url + '/account/submitConcern/'
		browser.get(url)
		title = browser.find_element_by_id('id_title')
		title.send_keys("concerns")
		agency = browser.find_element_by_id('id_agent')
		agency.send_keys("some agency")
		content = browser.find_element_by_id('id_content')
		content.send_keys("contents")
		browser.find_element_by_name('concern_submit_button').click()
		assert '/account/dashboard/' in browser.current_url

	def test_concern_emptytitle(self):
		browser = self.selenium
		url = self.live_server_url + '/account/submitConcern/'
		browser.get(url)
		title = browser.find_element_by_id('id_title')
		title.send_keys("")
		agency = browser.find_element_by_id('id_agent')
		agency.send_keys("some agency")
		content = browser.find_element_by_id('id_content')
		content.send_keys("contents")
		browser.find_element_by_name('concern_submit_button').click()
		assert '/submitConcern/' in browser.current_url
		assert 'should not be empty' in browser.page_source

	def test_concern_emptyagent(self):
		browser = self.selenium
		url = self.live_server_url + '/account/submitConcern/'
		browser.get(url)
		title = browser.find_element_by_id('id_title')
		title.send_keys("title")
		agency = browser.find_element_by_id('id_agent')
		agency.send_keys("")
		content = browser.find_element_by_id('id_content')
		content.send_keys("contents")
		browser.find_element_by_name('concern_submit_button').click()
		assert '/submitConcern/' in browser.current_url
		assert 'should not be empty' in browser.page_source

	def test_concern_emptycontent(self):
		browser = self.selenium
		url = self.live_server_url + '/account/submitConcern/'
		browser.get(url)
		title = browser.find_element_by_id('id_title')
		title.send_keys("title")
		agency = browser.find_element_by_id('id_agent')
		agency.send_keys("some agency")
		content = browser.find_element_by_id('id_content')
		content.send_keys("")
		browser.find_element_by_name('concern_submit_button').click()
		assert '/submitConcern/' in browser.current_url
		assert 'should not be empty' in browser.page_source

	def test_concern_badtitle(self):
		browser = self.selenium
		url = self.live_server_url + '/account/submitConcern/'
		browser.get(url)
		title = browser.find_element_by_id('id_title')
		title.send_keys("!!!")
		agency = browser.find_element_by_id('id_agent')
		agency.send_keys("some agency")
		content = browser.find_element_by_id('id_content')
		content.send_keys("some contents")
		browser.find_element_by_name('concern_submit_button').click()
		assert '/submitConcern/' in browser.current_url

	"""

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
		