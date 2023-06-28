from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

form_url = 'https://forms.gle/n1rAExdFBLirLkUB8'    # The url to the Data entry form
zillow_url = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'    # The zillow listings url

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
           "Accept-Language": "en-US,en;q=0.9"} # Browser headers

response = requests.get(url=zillow_url, headers=headers)    # Fetches the url, uses the headers specified
content = response.text     # Converts the website to base html code

soup = BeautifulSoup(content, "html.parser")    # Converts html code to BeautifulSoup object

properties = soup.find_all(name="div", class_="property-card-data")     # Finds all div elements with given class name
addresses = [property.find(name="address").getText().split("|")[-1].strip() for property in properties]    # Extract adderesses from the divs and formats text to remove uneccessary characters
prices = [property.find(name="span").getText().split("+")[0].split("/")[0].replace(",", '') for property in properties]     # Extract the price of each listing
urls = [property.find(name="a", class_="property-card-link").get('href') for property in properties]    # Get the urls of the listings

for url in urls:    
    if "https://www.zillow.com" not in url:
        urls[urls.index(url)] = "https://www.zillow.com" + url      # Fixes partial urls

driver = webdriver.Chrome()     # Creates Chrome driver for selenium

for property in range(len(properties)):     # Iterates through all the properties
    driver.get(form_url)    # Opens the form url
    driver.implicitly_wait(5)   # Sets implicitly wait for the Chrome driver
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))     # Waits for the input fields to load
    form_fields = [input for input in driver.find_elements(by=By.TAG_NAME, value="input") if input.get_attribute("type") == "text"]     # Appends all the form fields in a list
    form_fields[0].send_keys(addresses[property])   
    form_fields[1].send_keys(prices[property])
    form_fields[2].send_keys(urls[property])    # Fill the form fields with each data
    driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span").click()   # Clicks Submit button
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Submit another')))   # Waits for the submit page to come before reloading the form