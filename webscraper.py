from bs4 import BeautifulSoup
from selenium import webdriver
import selenium

def fetch_soup_from_page(url):
    while True:
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            page = driver.page_source
            driver.quit()
            soup = BeautifulSoup(page, 'html.parser')
            return soup
        except selenium.common.exceptions.TimeoutException:
            print("Timed out loading page, trying again")
        except selenium.common.exceptions.WebDriverException:
            print("Web Driver Error, trying again")