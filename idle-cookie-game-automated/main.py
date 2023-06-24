from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument("--log-level=3")   # Disable extra console prompts

driver = webdriver.Chrome(options=options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")
driver.implicitly_wait(5)

cookie = driver.find_element(by=By.ID, value="cookie")
score = driver.find_element(by=By.ID, value="money")
cps = driver.find_element(by=By.ID, value="cps")    # Cookies per second

end_time = time.time() + 60*5   # Sets the end time as 5 minutes from start
break_time = time.time() + 5    # Break has to be 5 seconds

while True:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#store div")))    # To avoid stale elements
    powerups = [driver.find_element(by=By.XPATH, value=f'//*[@id="store"]/div[{n}]') for n in range(1, 9)]
    powerups.pop()  # Last powerup is hidden by developer
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#store div b")))  # TO avoid stale elements
    prices = [int(price.text.split("-")[1].strip().replace(",", "")) for price in driver.find_elements(by=By.CSS_SELECTOR, value="#store div b")[:-1]]

    cookie.click()
    current_score = int(score.text.replace(",", ""))

    if time.time() >= break_time:   # If its 5 seconds past
        break_time = time.time() + 5    # Setting new break time
        for i in range(len(powerups)-1, -1, -1):  # Iterate backwards
            powerup = powerups[i]
            price = prices[i]
            if powerup.get_attribute("class") != "grayed" and price < current_score:
                powerup.click()
                break
    
    if time.time() >= end_time:
        break

print(f"You generate {cps.text} cookies/second")
time.sleep(5)

driver.quit()