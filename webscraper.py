from bs4 import BeautifulSoup
from selenium import webdriver
import selenium


def fetch_soup_from_page(url):
    while True:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1200x600')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            page = driver.page_source
            driver.quit()
            soup = BeautifulSoup(page, 'html.parser')
            return soup
        except selenium.common.exceptions.TimeoutException:
            print("Timed out loading page, trying again")
        except selenium.common.exceptions.WebDriverException:
            print("Web Driver Error, trying again")