from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import confidential

options = Options()     # Creates a class for WebDriver options
options.add_argument("--log-level=3")   # Disable extra console prompts

driver = webdriver.Chrome(options=options)  # Create the Chrome driver with the given options
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3632445688&f_AL=true&geoId=90000049&keywords=java%20developer&location=Los%20Angeles%20Metropolitan%20Area&refresh=true")    # Opens the LinkedIn job search page

driver.find_element(by=By.LINK_TEXT, value="Sign in").click()   # Opens login page
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))    # Finds username field
driver.find_element(by=By.ID, value="username").send_keys(confidential.EMAIL_ID)    # Enters the login email
driver.find_element(by=By.ID, value="password").send_keys(confidential.PASSWD)  # Enters password
driver.find_element(by=By.ID, value="password").send_keys(Keys.ENTER)   # Hits enter key

'''
If there is a captcha, the user will have to complete it and then hit enter in the console for the program to continue.
'''
if "Security Verification" in driver.title:
    input('Please complete security check, then hit enter: ')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[1]/div/ul/li[1]')))  # Waits until the first job listing is fully loaded
jobs = [driver.find_element(by=By.XPATH, value=f'//*[@id="main"]/div/div[1]/div/ul/li[{n}]') for n in range(1, 26)]     # Loads all job listings on that page in a list

for job in jobs:    # Iterates through all job listings
    driver.execute_script("arguments[0].scrollIntoView();", job)    # Scrolls to the listing
    try:
        job.click()     # Clicks on the job
    except:
        pass
    try:
        '''
        If the job has already been applied for it will not have a button of the class jobs-apply-button, so the script sees if the button is available and if not it catches the exception and continues to next job
        '''
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button")))   
        driver.execute_script('arguments[0].click()', driver.find_element(by=By.CLASS_NAME, value="jobs-apply-button"))
    except TimeoutException:
        continue

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))     # Waits for the application page to load up
    inputs = driver.find_elements(by=By.TAG_NAME, value="input")    # Finds all input fields
    [number.send_keys(9876543210) for number in inputs if "phoneNumber-nationalNumber" in str(number.get_attribute("class"))]   # Finds the phone number field, and enters the number
    if "Submit application" in [button.text for button in driver.find_elements(by=By.TAG_NAME, value='button')]:
        # If the application can be submitted directly, it will be submitted, else the application will be saved
        driver.execute_script('arguments[0].click()', driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/div/div[2]/div/div/form/footer/div[3]/button"))
    else:
        driver.execute_script('arguments[0].click()', driver.find_element(by=By.CLASS_NAME, value='artdeco-button--2'))
        driver.execute_script('arguments[0].click()', driver.find_element(by=By.CLASS_NAME, value='artdeco-button--2'))
        driver.execute_script('arguments[0].click()', driver.find_element(by=By.CLASS_NAME, value='artdeco-button'))
        save_button = driver.find_elements(by=By.CSS_SELECTOR, value=".artdeco-modal__actionbar--confirm-dialog button")[1]
        driver.execute_script('arguments[0].click()', save_button)
driver.quit()
