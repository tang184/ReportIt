from django.utils import timezone
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException


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

	def test_adminlogin1_profile(self):
		print("test_adminlogin1_profile")
		browser = self.selenium
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("admin")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin")
		browser.find_element_by_name('login-submit').click()	
		assert 'username' not in browser.page_source

	def test_adminlogin2_wrongpassword(self):
		print("test_adminlogin2_wrongpassword")
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

	def test_adminlogin3_notexist(self):
		print("test_adminlogin3_notexist")
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
	def test_reportersignup1_good_withoptional(self):
		print("test_reportersignup1_good_withoptional")
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
		pwc.send_keys("pass1234")
		ln = browser.find_element_by_name('legal_name')
		ln.send_keys("Tom")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()		
		assert 'Reporter Signup' not in browser.title

	def test_reportersignup2_good_withoutoptional(self):
		print("test_reportersignup2_good_withoutoptional")
		browser = self.selenium
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()		
		assert 'Reporter Signup' not in browser.title

	def test_reportersignup3_invalidusername(self):
		print("test_reportersignup3_invalidusername")
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
		ln = browser.find_element_by_name('legal_name')
		ln.send_keys("Tom")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()
		assert 'Reporter Signup' in browser.title
		
	
	def test_reportersignup4_invalidemail(self):
		print("test_reportersignup4_invalidemail")
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
		ln = browser.find_element_by_name('legal_name')
		ln.send_keys("Tom")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()		
		assert 'Reporter Signup' in browser.title
	
	def test_reportersignup5_dismatchpswd(self):
		print("test_reportersignup5_dismatchpswd")
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
		ln = browser.find_element_by_name('legal_name')
		ln.send_keys("Tom")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()		
		assert 'Reporter Signup' in browser.title

	def test_reportersignup6_dupuser(self):
		print("test_reportersignup6_dupuser")
		browser = self.selenium
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("admin")
		email = browser.find_element_by_name('email')
		email.send_keys('admin@example.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		ln = browser.find_element_by_name('legal_name')
		ln.send_keys("Tom")
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		browser.find_element_by_name('signup_submit').click()	
		assert 'Reporter Signup' in browser.title




	""" agent signup """
	def test_agentsignup1_good(self):
		print("test_agentsignup1_good")
		browser = self.selenium
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()
		assert 'Agent Signup' not in browser.title

	def test_agentsignup2_invalidusername(self):
		print("test_agentsignup2_invalidusername")
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
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()		
		assert 'Agent Signup' in browser.title

	def test_agentsignup3_invalidemail(self):
		print("test_agentsignup3_invalidemail")
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
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()		
		assert 'Agent Signup' in browser.title

	def test_agentsignup4_dismatchpswd(self):
		print("test_agentsignup4_dismatchpswd")
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
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()
		assert 'Agent Signup' in browser.title

	def test_agentsignup5_dupuser(self):
		print("test_agentsignup5_dupuser")
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
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()
		assert 'Agent Signup' in browser.title




	""" submit concerns """

	def test_concern1_good(self):
		print("test_concern1_good")
		browser = self.selenium
		# agent signup
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()

		# reporter signup
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# reporter login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408_2")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		browser.find_element_by_name('submitconcern').click()
		title = browser.find_element_by_name('title')
		title.send_keys("concerns")
		agent = Select(browser.find_element_by_name('agent'))
		agent.select_by_index(0)
		content = browser.find_element_by_name('content')
		content.send_keys("contents")
		browser.find_element_by_id('concern_submit_button').click()
		assert 'ReportIt' in browser.title

	def test_concern2_emptytitle(self):
		print("test_concern2_emptytitle")
		browser = self.selenium
		# agent signup
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()

		# reporter signup
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# reporter login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408_2")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		browser.find_element_by_name('submitconcern').click()
		title = browser.find_element_by_name('title')
		title.send_keys("")
		agent = Select(browser.find_element_by_name('agent'))
		agent.select_by_index(0)
		content = browser.find_element_by_name('content')
		content.send_keys("contents")
		browser.find_element_by_id('concern_submit_button').click()
		assert '/submitConcern/' in browser.current_url

	def test_concern3_emptyagent(self):
		print("test_concern3_emptyagent")
		browser = self.selenium
		# agent signup
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()

		# reporter signup
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# reporter login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408_2")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		browser.find_element_by_name('submitconcern').click()
		title = browser.find_element_by_name('title')
		title.send_keys("concerns")
		agent = Select(browser.find_element_by_name('agent'))
		content = browser.find_element_by_name('content')
		content.send_keys("")
		browser.find_element_by_id('concern_submit_button').click()
		assert '/submitConcern/' in browser.current_url

	def test_concern4_emptycontent(self):
		print("test_concern4_emptycontent")
		browser = self.selenium
		# agent signup
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()

		# reporter signup
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# reporter login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408_2")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		browser.find_element_by_name('submitconcern').click()
		title = browser.find_element_by_name('title')
		title.send_keys("concerns")
		agent = Select(browser.find_element_by_name('agent'))
		agent.select_by_index(0)
		content = browser.find_element_by_name('content')
		content.send_keys("")
		browser.find_element_by_id('concern_submit_button').click()
		assert '/submitConcern/' in browser.current_url

	def test_concern5_badtitle(self):
		print("test_concern5_badtitle")
		browser = self.selenium
		# agent signup
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()

		# reporter signup
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# reporter login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408_2")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		browser.find_element_by_name('submitconcern').click()
		title = browser.find_element_by_name('title')
		title.send_keys("!!!")
		agent = Select(browser.find_element_by_name('agent'))
		agent.select_by_index(0)
		content = browser.find_element_by_name('content')
		content.send_keys("contents")
		browser.find_element_by_id('concern_submit_button').click()
		assert '/submitConcern/' in browser.current_url



	""" actions to my concerns """
	def test_myconcerns1_view(self):
		print("test_myconcerns1_view")
		browser = self.selenium
		# agent signup
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()

		# reporter signup
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# reporter login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408_2")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		browser.find_element_by_name('submitconcern').click()
		title = browser.find_element_by_name('title')
		title.send_keys("title for my concern")
		agent = Select(browser.find_element_by_name('agent'))
		agent.select_by_index(0)
		content = browser.find_element_by_name('content')
		content.send_keys("noise is loud")
		browser.find_element_by_id('concern_submit_button').click()

		# wait for submit form
		wait = WebDriverWait(browser, 10)
		element = wait.until(EC.element_to_be_clickable((By.ID, 'viewmyconcerns')))
		# view my concerns
		browser.find_element_by_name('viewmyconcerns').click()
		assert 'title for my concern' in browser.page_source
		browser.find_element_by_id('view').click()
		assert 'noise is loud' in browser.page_source

	def test_myconcerns2_remove(self):
		print("test_myconcerns2_remove")
		browser = self.selenium
		# agent signup
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()

		# reporter signup
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# reporter login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408_2")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		browser.find_element_by_name('submitconcern').click()
		title = browser.find_element_by_name('title')
		title.send_keys("title for my concern")
		agent = Select(browser.find_element_by_name('agent'))
		agent.select_by_index(0)
		content = browser.find_element_by_name('content')
		content.send_keys("contents")
		browser.find_element_by_id('concern_submit_button').click()

		# wait for submit form
		wait = WebDriverWait(browser, 10)
		element = wait.until(EC.element_to_be_clickable((By.ID, 'viewmyconcerns')))
		# remove my concerns
		browser.find_element_by_name('viewmyconcerns').click()
		assert 'title for my concern' in browser.page_source
		browser.find_element_by_id('remove').click()
		assert 'Successfully deleted the concern!' in browser.page_source




	"""def test_myconcerns3_edit(self):
		browser = self.selenium
		# agent signup
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()

		# reporter signup
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# reporter login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408_2")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		browser.find_element_by_name('submitconcern').click()
		title = browser.find_element_by_name('title')
		title.send_keys("title for my concern")
		agent = Select(browser.find_element_by_name('agent'))
		agent.select_by_index(0)
		content = browser.find_element_by_name('content')
		content.send_keys("noise is loud")
		browser.find_element_by_id('concern_submit_button').click()

		# wait for submit form
		wait = WebDriverWait(browser, 10)
		element = wait.until(EC.element_to_be_clickable((By.ID, 'viewmyconcerns')))
		# view my concerns and edit
		browser.find_element_by_name('viewmyconcerns').click()
		assert 'title for my concern' in browser.page_source
		browser.find_element_by_id('view').click()
		assert 'noise is loud' in browser.page_source
		browser.find_element_by_name('edit').click()
		title = browser.find_element_by_name('title')
		title.send_keys("loud construction noise")
		agent = browser.find_element_by_name('agent')
		agent.send_keys("Tom")
		content = browser.find_element_by_name('content')
		content.send_keys("construction noise is loud")
		browser.find_element_by_id('concern_submit_button').click()
		# wait for submit form
		wait = WebDriverWait(browser, 10)
		element = wait.until(EC.presence_of_element_located((By.ID, "view")))
		#assert 'Successfully edited the concern!' in browser.page_source"""



	""" Edit Profile """

	def test_editprofile1_immd_good(self):
		print("test_editprofile1_immd_good")
		# signup
		browser = self.selenium
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408_2")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		# edit
		browser.find_element_by_name('profile').click()
		# here need button name
		browser.find_element_by_name('edit_button').click()
		gen = browser.find_element_by_name('gender')
		gen.send_keys("female")
		phone = browser.find_element_by_name('phone')
		phone.send_keys("7651111111")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		bio = browser.find_element_by_name('bio')
		bio.send_keys("hello!")
		# here need button name
		browser.find_element_by_name('update_button').click()
		assert 'female' in browser.page_source
		assert '7651111111' in browser.page_source
		assert 'first street' in browser.page_source
		assert 'hello!' in browser.page_source

	def test_editprofile2_goback_good(self):
		print("test_editprofile2_goback_good")
		browser = self.selenium
		# signup
		browser = self.selenium
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408_2")
		email = browser.find_element_by_name('email')
		email.send_keys('321@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408_2")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		# edit
		browser.find_element_by_name('profile').click()

		# here need button name
		browser.find_element_by_name('edit_button').click()
		gen = browser.find_element_by_name('gender')
		gen.send_keys("female")
		phone = browser.find_element_by_name('phone')
		phone.send_keys("7651111111")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		bio = browser.find_element_by_name('bio')
		bio.send_keys("hello!")
		# here need button name
		browser.find_element_by_name('update_button').click()

		# go to dashboard
		browser.find_element_by_name('dashboard').click()
		# back to profile page again
		browser.find_element_by_name('profile').click()
		assert 'female' in browser.page_source
		assert '7651111111' in browser.page_source
		assert 'first street' in browser.page_source
		assert 'hello!' in browser.page_source



	""" agent view directed concerns """
	def test_agentviewconcern1_good(self):
		print("test_agentviewconcern1_good")
		browser = self.selenium
		# reporter send concerns
		self.test_concern1_good()

		# reporter logout, agent login
		url = self.live_server_url + '/login/'
		browser.get(url)
		timeout = 10
		try:
			element_present = EC.presence_of_element_located((By.ID, 'id_username'))
			WebDriverWait(browser, timeout).until(element_present)
		except TimeoutException:
			print ("Timed out waiting for page to load")
			return
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		pswd = browser.find_element_by_name('password')
		pswd.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()
		browser.find_element_by_name('viewmyconcerns').click()
		assert "concerns" in browser.page_source

	def test_agentviewconcern2_resolve(self):
		print("test_agentviewconcern2_resolve")
		browser = self.selenium
		# reporter send concerns
		self.test_concern1_good()
		# reporter logout, agent login
		url = self.live_server_url + '/login/'
		browser.get(url)
		timeout = 10
		try:
			element_present = EC.presence_of_element_located((By.ID, 'id_username'))
			WebDriverWait(browser, timeout).until(element_present)
		except TimeoutException:
			print ("Timed out waiting for page to load")
			return
		un = browser.find_element_by_name('username')
		un.send_keys("agent1")
		pswd = browser.find_element_by_name('password')
		pswd.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()
		browser.find_element_by_name('viewmyconcerns').click()
		assert "concerns" in browser.page_source
		timeout = 10
		try:
			element_present = EC.presence_of_element_located((By.NAME, 'view'))
			WebDriverWait(browser, timeout).until(element_present)
		except TimeoutException:
			print ("Timed out waiting for page to load")
			return
		browser.find_element_by_name('view').click()
		browser.find_element_by_id('resolve_submit_button').click()
		browser.find_element_by_name('view').click()
		assert 'True' in browser.page_source



	""" view all concerns """
	def test_viewallconcerns1_reporter(self):
		print("test_viewallconcerns1_reporter")
		browser = self.selenium
		# reporter login
		# reporter submit concerns
		self.test_concern1_good()
		wait = WebDriverWait(browser, 10)
		element = wait.until(EC.presence_of_element_located((By.ID, 'welcome')))
		browser.find_element_by_name('submitconcern').click()
		title = browser.find_element_by_name('title')
		title.send_keys("construction noise")
		agent = Select(browser.find_element_by_name('agent'))
		agent.select_by_index(0)
		content = browser.find_element_by_name('content')
		content.send_keys("very very loud")
		browser.find_element_by_id('concern_submit_button').click()

		# view all concerns
		timeout = 5
		try:
			element_present = EC.presence_of_element_located((By.NAME, 'viewallconcerns'))
			WebDriverWait(browser, timeout).until(element_present)
		except TimeoutException:
			print ("Timed out waiting for page to load")
			return
		browser.find_element_by_name('viewallconcerns').click()
		assert 'concerns' in browser.page_source
		assert 'construction noise' in browser.page_source
		#assert 'broken bench' in browser.page_source


	""" view other's profile """
	def test_viewotherprofile1_reprep(self):
		print("test_viewotherprofile1_reprep")
		# agent signup
		browser = self.selenium
		url = self.live_server_url + '/agentSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("agent1")
		email = browser.find_element_by_name('email')
		email.send_keys('123@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		lname = browser.find_element_by_name('legal_name')
		lname.send_keys('Tom')
		phone = browser.find_element_by_name('phone_number')
		phone.send_keys("7652223333")
		add = browser.find_element_by_name('address')
		add.send_keys("first street")
		abt = browser.find_element_by_name('about')
		abt.send_keys("nice to meet you!")
		vfile = browser.find_element_by_id('file_input')
		vfile.send_keys("/Users/rainy/Desktop/logo.png")
		try:
			WebDriverWait(browser, 5).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
			alert = browser.switch_to.alert
			alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
		browser.find_element_by_name('signup_submit').click()

		# first reporter cs408 signup
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408")
		email = browser.find_element_by_name('email')
		email.send_keys('cs408@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# second reporter cs307 signup
		url = self.live_server_url + '/reporterSignup/'
		browser.get(url)
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs307")
		email = browser.find_element_by_name('email')
		email.send_keys('cs307@qq.com')
		pw = browser.find_element_by_name('password1')
		pw.send_keys("pass1234")
		pwc = browser.find_element_by_name('password2')
		pwc.send_keys("pass1234")
		browser.find_element_by_name('signup_submit').click()

		# cs408 login
		url = self.live_server_url + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("cs408")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		# cs408 submit concern
		browser.find_element_by_name('submitconcern').click()
		title = browser.find_element_by_name('title')
		title.send_keys("concerns")
		agent = Select(browser.find_element_by_name('agent'))
		agent.select_by_index(0)
		content = browser.find_element_by_name('content')
		content.send_keys("contents")
		browser.find_element_by_id('concern_submit_button').click()

		# cs307 login
		url = self.live_server_url + '/login/'
		browser.get(url)
		timeout = 10
		try:
			element_present = EC.presence_of_element_located((By.ID, 'id_username'))
			WebDriverWait(browser, timeout).until(element_present)
		except TimeoutException:
			print ("Timed out waiting for page to load")
			return
		un = browser.find_element_by_id('id_username')
		un.send_keys("cs408")
		pw = browser.find_element_by_name('password')
		pw.send_keys("pass1234")
		browser.find_element_by_name('login-submit').click()

		# cs307 view all concerns
		browser.find_element_by_name('viewallconcerns').click()
		browser.find_element_by_name('reporter_profile').click()
		assert 'cs408' in browser.page_source



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
		