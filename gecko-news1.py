import os
import time
import sys
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def google_news_search(query, max_results=2000):
    links = []
    driver = None

    try:
        driver = webdriver.Firefox()
        news_search_url = f"https://www.google.com/search?q={query}&tbm=nws"
        driver.get(news_search_url)

        while len(links) < max_results:
            time.sleep(random.uniform(2, 5))  # Random wait for results to load

            # Parse the page source and extract links
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            search_results = soup.find_all('a', class_='WlydOe')

            page_links = []
            for a in search_results:
                href = a.get('href')
                if href and href.startswith('https'):
                    if href not in links:
                        links.append(href)
                        page_links.append(href)
                        logging.debug(f"News link found - {href}")

            # Print the links from the current page
            for link in page_links:
                print(link)

            if len(links) >= max_results:
                break

            try:
                # Assuming "Next" button has text "Next" or "Уперед" as shown in the screenshot
                next_button = driver.find_element(By.XPATH, "//a[span[text()='Next' or text()='Уперед']]")
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                next_button.click()
                logging.info("Clicked the next button.")
            except NoSuchElementException:
                logging.info("No more pages or next button not found.")
                break

    except WebDriverException as e:
        logging.error(f"WebDriverException encountered: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if driver:
            driver.quit()
        logging.info("Browser closed.")

if __name__ == "__main__":
    search_query = sys.argv[1] if len(sys.argv) > 1 else "Test"
    google_news_search(search_query.replace(' ', '+'))

