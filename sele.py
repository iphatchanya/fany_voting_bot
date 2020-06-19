from selenium import webdriver
import time

def ChromeBot(username,password):
	driver = webdriver.Chrome(r'chromedriver')
	driver.maximize_window()

	# start login process
	driver.get("https://www.iheart.com/sdk/auth/?frame=ihr_bridge&signup=1&amp=https%3A%2F%2Fus.api.iheart.com")
	login_link = driver.find_element_by_xpath("//button[contains(text(),'Log In')]")
	login_link.click()
	login_form_user = driver.find_element_by_id("username")
	login_form_user.clear()
	login_form_user.send_keys(username)
	login_form_pass = driver.find_element_by_id("password")
	login_form_pass.clear()
	login_form_pass.send_keys(password)
	login_form_pass.submit()

	count = 0
	while count < 10: # check if logged in, goto voting page
		if driver.find_elements_by_xpath("//*[contains(text(), 'Sorry, an error occurred. Please try again later.')]") != []:
			print("[Error] Can't login user: %s" % (username))
			return False
		if driver.current_url == "data:,":
			break
		else:
			time.sleep(1)
		count = count + 1
	#end login process

	#start voting process
	driver.get("https://iheartawards.votenow.tv/?device_type=web&initialWidth=1903&childId=telescope-app&parentTitle=iHeartRadio%20Music%20Awards%20%7C%20iHeartRadio&parentUrl=https%3A%2F%2Fwww.iheart.com%2Fmusic-awards%2F%23vote#vote/4")
	
	#find tiffany button
	count = 0
	while count < 10:
		try:
			tiffany_button=driver.find_element_by_css_selector("[data-id='C1']")
			if tiffany_button != []:
				tiffany_button.click()
				break
			else:
				time.sleep(1)
		except Exception as e:
			time.sleep(1)
		count = count + 1

	count = 0
	while count < 10:
		try:
			votebutton = driver.find_element_by_xpath("//button[contains(text(),'CONFIRM VOTE')]")
			if votebutton != []:
				votebutton.click()
				break
			else:
				time.sleep(1)
		except Exception as e:
			time.sleep(1)
		count = count + 1

	count = 0
	while count < 10:
		try:
			if driver.find_elements_by_xpath("//*[contains(text(), 'Vote Again')]") != []:
				driver.close()
				return True
			else:
				time.sleep(1)
		except Exception as e:
			time.sleep(1)
		count = count + 1
	return False

f = open("userlist.txt", "r")
for x in f:
	if x.strip() != "":
		line = x.strip() # read file line by line and triming space at the end of file.
		username = line.split(',')[0] # split line with comma and get username (index - 0)
		password = line.split(',')[1] # split line with comma and get password (index - 1)
		voteresult = ChromeBot(username,password) # call bot function by passing username and password into function.
		if voteresult:
			print("User: %s voted" % (username))
		else:
			print("[Error] User: %s not voted" % (username))