# playwright_parfumo_xhr_check.py

from playwright.sync_api import sync_playwright
import json

TARGET_URL = "https://www.parfumo.com/Perfumes/Perfumeria_Gal/Classe_Eau_de_Toilette"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True로 바꿔도 됨
        page = browser.new_page()

        def handle_response(response):
            try:
                url = response.url
                if any(k in url.lower() for k in ["review", "comment", "rating", "ajax", "api"]):
                    print("\n[XHR DETECTED]")
                    print("URL:", url)
                    print("STATUS:", response.status)
                    ct = response.headers.get("content-type", "")
                    print("Content-Type:", ct)
                    if "json" in ct:
                        try:
                            data = response.json()
                            print("JSON KEYS:", list(data.keys()) if isinstance(data, dict) else type(data))
                        except:
                            print("JSON parse failed")
            except:
                pass

        page.on("response", handle_response)

        page.goto(TARGET_URL, wait_until="networkidle")
        page.wait_for_timeout(3000)

        # 스크롤로 리뷰 로딩 유도
        for _ in range(5):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(2000)

        print("\n[END] Network inspection finished")
        browser.close()

if __name__ == "__main__":
    main()