from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import requests
from bs4 import BeautifulSoup

CHROMIUM_PATH = "/usr/bin/chromium-browser"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

def get_email_from_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", soup.get_text()))
        return list(emails)[0] if emails else "Not found"
    except:
        return "Not found"

def scrape_google_maps(keyword, location):
    options = Options()
    options.binary_location = CHROMIUM_PATH
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0")

    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.com/maps")
    time.sleep(2)

    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.clear()
    search_box.send_keys(f"{keyword} in {location}")
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    results = []
    listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/place")]')[:10]

    for i in range(len(listings)):
        try:
            listings[i].click()
            time.sleep(4)

            try:
                name = driver.find_element(By.XPATH, '//h1[contains(@class,"DUwDvf")]').text
            except:
                name = "N/A"

            try:
                address = driver.find_element(By.XPATH, '//div[contains(@class,"Io6YTe") and contains(text(),",")]').text
            except:
                address = "N/A"

            try:
                website_button = driver.find_element(By.XPATH, '//a[contains(@data-value,"Website")]')
                website_url = website_button.get_attribute('href')
            except:
                website_url = ""

            email = get_email_from_website(website_url) if website_url else "Not found"

            results.append({
                "Business Name": name,
                "Address": address,
                "Maps URL": driver.current_url,
                "Email": email
            })

            driver.back()
            time.sleep(3)
            listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/place")]')[:10]

        except:
            continue

    driver.quit()
    return results
