import time
import random
import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


class FragranticaScraper:
    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.data = []

    def scrape(self, url, max_scroll=5):
        try:
            self.driver.get(url)
            time.sleep(3)

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            perfume_name, brand = self._extract_name_brand(soup)
            accords = self._extract_accords(soup)

            # 🔴 핵심 1: Reviews 탭 클릭
            self._click_reviews_tab()

            # 🔴 핵심 2: 리뷰 로드
            self._load_reviews(max_scroll)

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            self._extract_reviews(soup, perfume_name, brand, accords)

        finally:
            self.driver.quit()

        return pd.DataFrame(self.data)

    def _click_reviews_tab(self):
        try:
            tab = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(text(), 'Ratings') or contains(text(), 'Reviews')]")
                )
            )
            tab.click()
            time.sleep(3)
        except Exception as e:
            print("❌ Reviews tab click failed:", e)

    def _extract_name_brand(self, soup):
        h1 = soup.find("h1")
        if not h1:
            return None, None

        text = h1.get_text(strip=True)
        if "(" in text and ")" in text:
            name = text.split("(")[0].strip()
            brand = text.split("(")[1].replace(")", "").strip()
        else:
            name = text
            brand = None

        return name, brand

    def _extract_accords(self, soup):
        span = soup.find("span", itemprop="keywords")
        return span.get_text(strip=True) if span else None

    def _load_reviews(self, max_scroll):
        for _ in range(max_scroll):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(random.uniform(2, 4))

            try:
                btn = self.driver.find_element(
                    By.XPATH, "//button[contains(., 'Load')]"
                )
                btn.click()
                time.sleep(random.uniform(2, 4))
            except:
                pass

    def _extract_reviews(self, soup, perfume, brand, accords):
        # itemprop 기반 + class 기반 모두 탐색
        review_blocks = soup.find_all(
            ["div", "article"],
            attrs={
                "itemprop": "review"
            }
        )

        if not review_blocks:
            review_blocks = soup.find_all(
                "div", class_=re.compile("review", re.I)
            )

        print(f"🔍 Found review blocks: {len(review_blocks)}")

        for block in review_blocks:
            p = block.find("p")
            if not p:
                continue

            text = p.get_text(strip=True)
            if len(text) < 30:
                continue

            rating = self._extract_rating(block)
            date = self._extract_date(block)

            self.data.append({
                "perfume": perfume,
                "brand": brand,
                "accords": accords,
                "review_text": text,
                "rating": rating,
                "date": date
            })

    def _extract_rating(self, block):
        span = block.find("span", itemprop="ratingValue")
        if span:
            try:
                return float(span.get_text(strip=True))
            except:
                return None
        return None

    def _extract_date(self, block):
        time_tag = block.find("time")
        return time_tag.get_text(strip=True) if time_tag else None


if __name__ == "__main__":
    url = "https://www.fragrantica.com/perfume/Tom-Ford/Black-Orchid-1446.html"

    scraper = FragranticaScraper(headless=True)
    df = scraper.scrape(url, max_scroll=5)

    print(df.head())
    print(f"Total reviews: {len(df)}")

    df.to_csv("fragrantica_reviews.csv", index=False, encoding="utf-8")