import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from Genlogin import Genlogin

class ShopeeCrawler:
    def __init__(self, profile_id=None):
        self.driver = None
        self.gen = Genlogin("")
        self.profile_id = profile_id  # Cho phép truyền profile_id bên ngoài

    def _human_delay(self, min_delay=1.5, max_delay=4.5):
        time.sleep(random.uniform(min_delay, max_delay) + random.random())

    def _get_user_agents(self):
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        ]

    def _start_stealth_browser(self):
        try:
            # Nếu chưa truyền profile_id, lấy profile đầu tiên
            if not self.profile_id:
                profile_data = self.gen.getProfiles(0, 1)
                if not profile_data.get("profiles"):
                    raise Exception("Không tìm thấy profile")
                self.profile_id = profile_data["profiles"][0]["id"]
            # Chạy profile được chỉ định
            run_data = self.gen.runProfile(self.profile_id)
            if not run_data.get("wsEndpoint"):
                raise Exception("Không thể khởi chạy profile")
            debugger_address = run_data["wsEndpoint"].replace("ws://", "").split("/")[0]
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", debugger_address)
            options.add_argument(f"user-agent={random.choice(self._get_user_agents())}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-infobars")
            service = Service('crawl/chromedriver.exe')
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print(f"Khởi động trình duyệt thành công với profile {self.profile_id}")
        except Exception as e:
            print(f"Lỗi khởi động trình duyệt: {str(e)}")
            raise

    def _shopee_behavior(self):
        for _ in range(random.randint(2, 5)):
            self.driver.execute_script(f"window.scrollBy(0, {random.randint(300, 600)})")
            self._human_delay(0.6, 1.2)
            ActionChains(self.driver).move_by_offset(random.randint(10, 100), random.randint(10, 100)).perform()
            self._human_delay(0.4, 1.1)
            try:
                logo = self.driver.find_element(By.CSS_SELECTOR, "a.navbar__logo")
                ActionChains(self.driver).move_to_element(logo).click().perform()
            except Exception:
                pass

    def _handle_captcha(self):
        print("Phát hiện CAPTCHA! Hãy giải Captcha thủ công trên trình duyệt (kéo thanh hoặc click hình), rồi nhấn Enter để tiếp tục...")
        input("Sau khi giải xong Captcha trên trình duyệt, nhấn Enter để tiếp tục...")

    def _extract_reviews(self):
        reviews = []
        page = 1
        while True:
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.shopee-product-rating"))
                )
                self._human_delay(0.7, 1.5)
                for el in self.driver.find_elements(By.CSS_SELECTOR, "div.shopee-product-rating"):
                    try:
                        content = el.find_element(By.CSS_SELECTOR, ".shopee-product-rating__main").text
                    except Exception:
                        content = ""
                    try:
                        rating = len(el.find_elements(By.CSS_SELECTOR, ".icon-rating-solid--active"))
                    except Exception:
                        rating = None
                    try:
                        author = el.find_element(By.CSS_SELECTOR, ".shopee-product-rating__author-name").text
                    except Exception:
                        author = ""
                    try:
                        date = el.find_element(By.CSS_SELECTOR, ".shopee-product-rating__time").text
                    except Exception:
                        date = ""
                    reviews.append({
                        "content": content,
                        "rating": rating,
                        "author": author,
                        "date": date,
                        "page": page
                    })
                next_btn = self.driver.find_elements(By.CSS_SELECTOR, ".shopee-icon-button.shopee-icon-button--right")
                if next_btn and next_btn[0].is_enabled():
                    next_btn[0].click()
                    page += 1
                    self._human_delay(1.2, 2.8)
                else:
                    break
            except Exception as e:
                print(f" Lỗi trích xuất trang review: {str(e)}")
                break
        return reviews

    def crawl(self, product_url):
        try:
            if not product_url.startswith(("http://", "https://")):
                product_url = f"https://{product_url}"
            self._start_stealth_browser()
            self.driver.get(product_url)
            self._human_delay(2, 3)
            # Nếu bị captcha
            while "verify" in self.driver.current_url or "captcha" in self.driver.title.lower():
                self._handle_captcha()
                self.driver.get(product_url)
                self._human_delay(2, 3)
            self._shopee_behavior()
            reviews = self._extract_reviews()
            return reviews
        except Exception as e:
            print(f" Lỗi tổng: {str(e)}")
            return []
        finally:
            if self.driver:
                self.driver.quit()
            if self.profile_id:
                self.gen.stopProfile(self.profile_id)

if __name__ == "__main__":
    # Hiển thị danh sách profile để chọn
    gen = Genlogin("")
    profiles = gen.getProfiles(0, 20).get("profiles", [])
    if not profiles:
        print("Không có profile nào trong Genlogin.")
        exit(1)
    print("Danh sách profile:")
    for i, profile in enumerate(profiles):
        # In ra để biết chắc key nào là tên
        print(f"{i+1}. {profile.get('profileName') or profile.get('title') or profile.get('name') or 'NoName'} (id: {profile.get('id') or profile.get('profile_id')})")
    idx = int(input("Nhập số thứ tự profile muốn dùng: ")) - 1
    profile_id = profiles[idx].get('id') or profiles[idx].get('profile_id')

    product_url = input("Nhập URL sản phẩm Shopee: ").strip()
    crawler = ShopeeCrawler(profile_id=profile_id)
    reviews = crawler.crawl(product_url)
    if reviews:
        pd.DataFrame(reviews).to_csv("shopee_reviews.csv", index=False)
        print(f"Crawl thành công {len(reviews)} đánh giá!")
    else:
        print("Không tìm thấy đánh giá nào!")