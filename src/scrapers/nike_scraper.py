import undetected_chromedriver as uc
uc.Chrome.__del__ = lambda self: None

from webdriver_manager.core.os_manager import OperationSystemManager, ChromeType

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

from pathlib import Path

import random
import time

class TrainingScraper:
    # Initialize driver properties
    def __init__(self, url:str):
        self.url = url
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]

        self.options = uc.ChromeOptions()
        self.options.add_argument(f"--user-agent={random.choice(user_agents)}")
        self.options.add_argument("--headless")
        self.options.add_argument("--lang=en-EN")
        self.options.add_argument("--disable-features=Translate")

        version = OperationSystemManager().get_browser_version_from_os(ChromeType.GOOGLE)
        self.main_version = int(version.split('.')[0])
        self.driver = uc.Chrome(options=self.options, version_main=self.main_version)
        self.wait = WebDriverWait(self.driver, 12)

        self.data = {}

    # Open url in browser
    def fetch_page(self):
        try:
            self.driver.get(self.url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("Main loaded")
        except:
            print("Main didn't load")

    # Close cookies window
    def accept_cookies(self):
        cookies_locator = (By.CSS_SELECTOR, "[aria-label*='Accept All']")
        accept_button = self.wait.until(EC.presence_of_element_located(cookies_locator))
        accept_button.click()

    # Find imgs srcs to download
    def catch_training_data(self):
        self.load_imgs()

        imgs_locator = (By.CSS_SELECTOR, "img[class*='product-card__hero-image']")
        imgs = self.driver.find_elements(*imgs_locator)
        print(f"Se encontraron {len(imgs)} imágenes.")

        i = 1
        for img in imgs:
            src = img.get_attribute("src")
            if src:
                self.download_img(src, f"jordan_{i}.jpg")
                i += 1

    # Scroll to load imgs
    def load_imgs(self):
        imgs_locator = (By.CSS_SELECTOR, "img[class*='product-card__hero-image']")

        loaded_imgs = 0
        i = 0

        while i < 6 or loaded_imgs == len(self.driver.find_elements(*imgs_locator)):
            self.driver.execute_script(f"window.scrollBy(0, {random.uniform(500, 1500)})")
            time.sleep(random.uniform(1, 2.5))
            i += 1

    # Save img in raw data
    def download_img(self, src, file_name):
        base_dir = Path(__file__).parent.parent.parent
        dir_path = base_dir / "data" / "raw" / "jordan_panda"

        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / file_name

        try:
            response = requests.get(url=src, timeout=10)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {file_name}")
        except Exception as e:
            print(f"Error downloading: {e}")        

    def close(self):
        try:
            self.driver.quit()
        except:
            print("Driver is already closed")

def nike_scrap():
    url = "https://www.nike.com/w/4g797z90poy?q=jordan%20panda"
    scraper = TrainingScraper(url)

    scraper.fetch_page()
    scraper.accept_cookies()
    scraper.catch_training_data()
    scraper.close()