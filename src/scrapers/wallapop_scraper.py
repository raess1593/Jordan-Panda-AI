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

class WallapopScraper:
    def __init__(self, url:str):
        self.url = url
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]

        self.options = uc.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument(f"--user-agent={random.choice(user_agents)}")
        self.options.add_argument("--lang=en-EN")
        self.options.add_argument("--disable-features=Translate")
        
        version = OperationSystemManager().get_browser_version_from_os(ChromeType.GOOGLE)
        self.main_version = int(version.split('.')[0])
        self.driver = uc.Chrome(options=self.options, version_main=self.main_version)
        self.wait = WebDriverWait(self.driver, 10)

    def open_url(self):
        try:
            self.driver.get(self.url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(random.uniform(0.5, 1.5))
        except:
            print(f"Error loading url: {self.url}")
        else:
            print("Web loaded successfully")

    def accept_cookies(self):
        try:
            shadow_host = self.wait.until(EC.presence_of_element_located((By.ID, "cmpwrapper")))
            shadow_root = shadow_host.shadow_root

            time.sleep(1) 
            accept_button = shadow_root.find_element(By.ID, "cmpwelcomebtnyes")
            accept_button.click()
            print("Cookies accepted")
        except:
            pass

    def scrape(self):
        for _ in range(4):
            self.driver.execute_script(f"window.scrollBy(0, {random.uniform(500, 2000)})")
            time.sleep(random.uniform(1, 2))

        grid = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='ItemCardGrid']")))
        imgs = grid.find_elements(By.CSS_SELECTOR, "[class*='item-card-image']")
        
        root_path = Path(__file__).parent.parent.parent
        data_path = root_path / "data" / "raw" / "jordan_panda"
        data_path.mkdir(parents=True, exist_ok=True)
    
        i = 1

        for img in imgs:
            src = img.get_attribute("src")
            if src:
                response = requests.get(url=src, timeout=5)
                if response.status_code == 200:
                    file_name = f"jordan_wallapop_{i}.jpg"
                    file_path = data_path / file_name
                    i += 1
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                        print(f"\tDownloaded: {file_name}")
                    if i > 50:
                        break

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = WallapopScraper(url="https://es.wallapop.com/search?keywords=jordan+panda&order_by=most_relevance")
    scraper.open_url()
    scraper.accept_cookies()
    scraper.scrape()
    scraper.close()