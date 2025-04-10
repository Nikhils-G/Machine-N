
from playwright.sync_api import sync_playwright
import re
import requests
from bs4 import BeautifulSoup

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
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        search_query = f"{keyword} in {location}"
        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(4000)

        page.fill("input#searchboxinput", search_query)
        page.keyboard.press("Enter")
        page.wait_for_timeout(6000)

        listings = page.locator('//a[contains(@href, "/place")]')
        count = listings.count()

        for i in range(min(10, count)):
            try:
                link = listings.nth(i)
                link.click()
                page.wait_for_timeout(4000)

                try:
                    name = page.locator('//h1[contains(@class,"DUwDvf")]').first.text_content()
                except:
                    name = "N/A"

                try:
                    address = page.locator('//div[contains(@class,"Io6YTe") and contains(text(),",")]').first.text_content()
                except:
                    address = "N/A"

                try:
                    website_button = page.locator('//a[contains(@data-value,"Website")]').first
                    website_url = website_button.get_attribute("href")
                except:
                    website_url = ""

                email = get_email_from_website(website_url) if website_url else "Not found"

                results.append({
                    "Business Name": name,
                    "Address": address,
                    "Maps URL": page.url,
                    "Email": email
                })

                page.go_back()
                page.wait_for_timeout(3000)
                listings = page.locator('//a[contains(@href, "/place")]')
            except:
                continue

        browser.close()

    return results
