form_url = 'https://forms.gle/n1rAExdFBLirLkUB8'
zillow_url = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43", "Accept-Language": "en-US,en;q=0.9"}

response = requests.get(url=zillow_url, headers=headers)
content = response.text

soup = BeautifulSoup(content, "html.parser")

properties = soup.find_all(name = "div", class_ = "property-card-data")
addresses = [property.find(name = "address").getText().split("|")[-1].strip() for property in 
properties]
prices = [property.find(name = "span").getText().split("+")[0].split("/")[0].replace(",", '') for property in 
properties]
urls = [property.find(name = "a", class_ = "property-card-link").get('href') for property in properties]
for url in urls:
    if "https://www.zillow.com" not in url:
        urls[urls.index(url)] = "https://www.zillow.com" + url

driver = webdriver.Chrome()

for property in range(len(properties)):
    driver.get(form_url)
    driver.implicitly_wait(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    form_fields = [input for input in driver.find_elements(by=By.TAG_NAME, value="input") if input.get_attribute("type") == "text"]
    form_fields[0].send_keys(addresses[property])
    form_fields[1].send_keys(prices[property])
    form_fields[2].send_keys(urls[property])
    driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Submit another')))