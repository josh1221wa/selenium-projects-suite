from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import confidential

options = Options()
options.add_argument("--log-level=3")   # Disable extra console prompts

driver = webdriver.Chrome(options=options)
# driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3632445688&f_AL=true&geoId=90000049&keywords=java%20developer&location=Los%20Angeles%20Metropolitan%20Area&refresh=true")

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3632445688&f_AL=true&geoId=90000049&keywords=java%20developer&location=Los%20Angeles%20Metropolitan%20Area&refresh=true")

driver.find_element(by=By.LINK_TEXT, value="Sign in").click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
driver.find_element(by=By.ID, value="username").send_keys(confidential.EMAIL_ID)
driver.find_element(by=By.ID, value="password").send_keys(confidential.PASSWD)
driver.find_element(by=By.ID, value="password").send_keys(Keys.ENTER)


if "Security Verification" in driver.title:
    input('Please complete security check, then hit enter: ')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[1]/div/ul/li[1]')))
jobs = [driver.find_element(by=By.XPATH, value=f'//*[@id="main"]/div/div[1]/div/ul/li[{n}]') for n in range(1, 26)]

for job in jobs:
    driver.execute_script("arguments[0].scrollIntoView();", job)
    try:
        job.click()
    except:
        pass
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button")))
        driver.execute_script('arguments[0].click()', driver.find_element(by=By.CLASS_NAME, value="jobs-apply-button"))
    except TimeoutException:
        continue
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    inputs = driver.find_elements(by=By.TAG_NAME, value="input")
    [number.send_keys(9876543210) for number in inputs if "phoneNumber-nationalNumber" in str(number.get_attribute("class"))]
    if "Submit application" in [button.text for button in driver.find_elements(by=By.TAG_NAME, value='button')]:
        driver.execute_script('arguments[0].click()', driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/div/div[2]/div/div/form/footer/div[3]/button"))
    else:
        driver.execute_script('arguments[0].click()', driver.find_element(by=By.CLASS_NAME, value='artdeco-button--2'))
        driver.execute_script('arguments[0].click()',driver.find_element(by=By.CLASS_NAME, value='artdeco-button--2'))
        driver.execute_script('arguments[0].click()',driver.find_element(by=By.CLASS_NAME, value='artdeco-button'))
        save_button = driver.find_elements(by=By.CSS_SELECTOR, value=".artdeco-modal__actionbar--confirm-dialog button")[1]
        driver.execute_script('arguments[0].click()', save_button)
driver.quit()