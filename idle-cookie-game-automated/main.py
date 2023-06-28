from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()     # Creates a class for WebDriver options
options.add_argument("--log-level=3")   # Disable extra console prompts

driver = webdriver.Chrome(options=options)  # Create the Chrome driver
driver.get("http://orteil.dashnet.org/experiments/cookie/")     # Open the cookie game website
driver.implicitly_wait(5)

cookie = driver.find_element(by=By.ID, value="cookie")  # Find the clickable cookie button
score = driver.find_element(by=By.ID, value="money")    # Find the money counter score board
cps = driver.find_element(by=By.ID, value="cps")    #  Finds the cookies per second score board

end_time = time.time() + 60*5   # Sets the end time as 5 minutes from start
break_time = time.time() + 5    # Break has to be 5 seconds

while True:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#store div")))    # To avoid the variable from holding stale elements 
    powerups = [driver.find_element(by=By.XPATH, value=f'//*[@id="store"]/div[{n}]') for n in range(1, 9)]      # Gets th powerip list
    powerups.pop()  # Last powerup is hidden by developer
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#store div b")))  # To avoid the variable from holding stale elements 
    prices = [int(price.text.split("-")[1].strip().replace(",", "")) for price in driver.find_elements(by=By.CSS_SELECTOR, value="#store div b")[:-1]]  # All the prices of the powerups

    cookie.click()  # Clicks the cookie every while loop
    current_score = int(score.text.replace(",", ""))    # Gets the current score

    if time.time() >= break_time:   # If its past 5 seconds
        break_time = time.time() + 5    # Setting new break time
        for i in range(len(powerups)-1, -1, -1):  # Iterate through powerups backwards
            powerup = powerups[i]
            price = prices[i]
            if powerup.get_attribute("class") != "grayed" and price < current_score:    # If powerup is available and affordable
                powerup.click()     # It clicks on the powerup
                break   # Breaks earlier iteration

    if time.time() >= end_time:     # If time crosses 5 minutes
        break   # Breaks the program

print(f"You generate {cps.text} cookies/second")    # Prints cookies/second
time.sleep(5)   # Sleeps for 5 seconds
driver.quit()   # Closes web driver
