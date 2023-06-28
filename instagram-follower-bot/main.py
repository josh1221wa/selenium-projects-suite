from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import confidential     # Is a custom module which contains all usernames, passwords and other private information


class InstaFollower:    # Created a class for the execution of this project
    def __init__(self):
        self.driver = webdriver.Chrome()    # The Chrome driver is made as a driver attribute of the class

    def login(self):    # The class method used to login to Instagram
        driver = self.driver    # Just to avoid using self.driver over and over
        driver.get("https://www.instagram.com/accounts/login/")     # Opens the instagram login page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))  # Waits till login page is fully loaded
        driver.find_element(by=By.NAME, value="username").send_keys(confidential.USERNAME)  # Enters username
        driver.find_element(by=By.NAME, value="password").send_keys(confidential.PASSWORD)  # Enters password
        driver.find_element(by=By.NAME, value="password").send_keys(Keys.ENTER)     # Hits the enter key
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "verificationCode")))  # Waits for the 2FA page to load
        driver.find_element(by=By.NAME, value="verificationCode").send_keys(input('Enter Verification Code: '))     # Asks the user for the 2FA code and then enters it in the page
        driver.find_element(by=By.NAME, value="verificationCode").send_keys(Keys.ENTER)     # Hits the enter key
        while "Login" in driver.title:  # Waits till login is fully complete
            pass
        time.sleep(5)

    def find(self):     # Finds the account to follow
        self.driver.get(f"https://www.instagram.com/{confidential.ACCOUNT}")    # Goes to the account page
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a')))     # Waits for the whole page to load
        self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a').click()  # Clicks on the followers button

    def follow(self):   # Follows all accounts
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div/div[3]/div/button')))    # Waits for the first follower to load
        count = 1   # Iterates through all the followers
        tryAgain = 0    # If faces with error, it tries the whole block again to make sure
        while tryAgain != 1:
            try:
                while True:
                    try:
                        button = self.driver.find_element(by=By.XPATH, value=f'/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{count}]/div/div/div/div[3]/div/button')     # Finds each follower button by path
                        self.driver.execute_script("arguments[0].scrollIntoView();", button)    # Scrolls to the follow button
                        button.click()  # Clicks the follow button
                        tryAgain = 0    # tryAgain is set to zero since there is no error
                    except ElementClickInterceptedException:
                        WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/button[2]')))   # If the account is already followed just click cancel unfollow button
                        self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/button[2]').click()
                    finally:
                        count += 1  # Increases count

            except NoSuchElementException:  # If theres no element existing i.e. no more to follow
                time.sleep(10)
                tryAgain = 1


bot = InstaFollower()   # Creates the object
bot.login()
bot.find() 
bot.follow()
bot.driver.quit()   # Closes WebDriver
