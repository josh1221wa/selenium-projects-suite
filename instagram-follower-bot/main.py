from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import confidential

class InstaFollower:
    def __init__(self):
        self.driver = webdriver.Chrome()
    
    def login(self):
        driver = self.driver    # Just to avoid using self.driver over and over
        driver.get("https://www.instagram.com/accounts/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(by=By.NAME, value="username").send_keys(confidential.USERNAME)
        driver.find_element(by=By.NAME, value="password").send_keys(confidential.PASSWORD)

        driver.find_element(by=By.NAME, value="password").send_keys(Keys.ENTER)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "verificationCode")))
        driver.find_element(by=By.NAME, value="verificationCode").send_keys(input('Enter Verification Code: '))
        driver.find_element(by=By.NAME, value="verificationCode").send_keys(Keys.ENTER)
        while "Login" in driver.title:
            pass
        time.sleep(5)

    def find(self):
        self.driver.get(f"https://www.instagram.com/{confidential.ACCOUNT}")
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a')))
        self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a').click()

    def follow(self):
        pass
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div/div[3]/div/button')))
        count = 1
        tryAgain = 0
        while tryAgain != 1:
            try:
                while True:
                    try:
                        button = self.driver.find_element(by = By.XPATH, value=f'/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{count}]/div/div/div/div[3]/div/button')
                        self.driver.execute_script("arguments[0].scrollIntoView();", button)
                        button.click()
                        tryAgain = 0
                    except ElementClickInterceptedException:
                        WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/button[2]')))
                        self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/button[2]').click()
                    finally:
                        count += 1

            except NoSuchElementException:
                time.sleep(10)
                tryAgain = 1



        
bot = InstaFollower()
bot.login()
bot.find()
bot.follow()
bot.driver.quit()