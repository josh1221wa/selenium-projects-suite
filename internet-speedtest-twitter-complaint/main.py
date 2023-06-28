from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import confidential     # Is a custom module which contains all usernames, passwords and other private information


class InternetSpeedTwitterBot:      # Creates a class for project execution
    def __init__(self):
        self.driver = webdriver.Chrome()    # Creates Chrome driver as class attribute
        self.speed = confidential.PROMISED_SPEED    # Stores the promised speed from the provider as class attribute

    def get_internet_speed(self):   # The method which fetches the internet speed
        self.driver.get("https://www.speedtest.net/")       # Opens speedtest.net
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "js-start-test")))      # Waits till the "Go" button is loaded and clickable
        self.driver.find_element(by=By.CLASS_NAME, value="js-start-test").click()   # Clicks the "Go" button
        while "result" not in self.driver.current_url:      # Waits till result loads
            pass

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')))    # Waits till the result is shown on screen

        download_speed = self.driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text       # Extracts the download speed from the site
        upload_speed = self.driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text     # Extracts the upload speed from the site

        return float(download_speed), float(upload_speed)       # Returns the upload and download speed

    def tweet_at_provider(self, text):      # The method to send the tweet, has an attribute text
        self.driver.get("https://twitter.com/i/flow/login")     # Opens twitter login page
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')))     # Waits for login page to fully load
        self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input').send_keys(confidential.EMAIL)    # Enters login Email
        self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input').send_keys(Keys.ENTER)        # Hits enter key

        try:
            '''
            Sometimes Twitter conducts double verification by asking the user to enter their twitter account username. In this try-except block the driver searches for form field to enter username and if found, it enters the username and hits enter. If not found it will just continue to the password step without throwing any errors.
            '''

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div/div/span/span')))
            self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input').send_keys(confidential.USERNAME)
            self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div').click()
        except TimeoutException:
            pass

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))     # Waits till password entry is visible
        self.driver.find_element(by=By.NAME, value="password").send_keys(confidential.PASSWD)   # Enters password in the field
        self.driver.find_element(by=By.NAME, value="password").send_keys(Keys.ENTER)    # Hits enter and submits

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div')))     # Waits till the tweet input field is loaded
        self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div').send_keys(text)      # Inputs the given text in the tweet input field
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[3]')))       # Finds the Post button
        self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[3]').click()    # Clicks on "Post"


bot = InternetSpeedTwitterBot()
down, up = bot.get_internet_speed()
if down < confidential.PROMISED_SPEED or up < confidential.PROMISED_SPEED:
    msg = f"Hey Internet Provider, why is my internet speed {down}down/{up}up when I paid for {confidential.PROMISED_SPEED}down/up?"
    bot.tweet_at_provider(msg)

time.sleep(10)
bot.driver.quit()
