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

'''
CODE NÀY CHƯA VƯỢT QUA ĐƯỢC PHẦN CAPTCHA CỦA SHOPEE, DO BỊ DETECT LÀ BOT
'''

class ShopeeCrawler:
    def __init__(self):
        self.driver = None
        self.gen = Genlogin("")
        self.profile_id = None

    def _human_delay(self):
        '''Tạo độ trễ ngẫu nhiên giữa các thao tác cho giống người thật'''
        time.sleep(random.uniform(1.5, 4.5) + random.random())

    def _start_stealth_browser(self):
        '''Làm theo document của genlogin'''
        try:
            # Lấy profile từ Genlogin
            profile_data = self.gen.getProfiles(0, 1)
            if not profile_data.get("profiles"):
                raise Exception("Không tìm thấy profile")
            self.profile_id = profile_data["profiles"][0]["id"]
            
            # chạy profile và lấy endpoint
            run_data = self.gen.runProfile(self.profile_id)
            if not run_data.get("wsEndpoint"):
                raise Exception("Không thể khởi chạy profile")
            
            # xử lý endpoint
            debugger_address = run_data["wsEndpoint"].replace("ws://", "").split("/")[0]
            
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", debugger_address)
            options.add_argument(f"user-agent={random.choice(self._get_user_agents())}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            service = Service('chromedriver.exe')
            self.driver = webdriver.Chrome(
                service=service, 
                options=options
            )
            print("Khởi động trình duyệt thành công")
            
        except Exception as e:
            print(f"Lỗi khởi động trình duyệt: {str(e)}")
            raise

    #test xem có chạy hiệu quả không
    def _get_user_agents(self):
        
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        ]

    def _shopee_behavior(self):
        # giả lập thao tác người thật: cuộn trang, di chuyển chuột ngẫu nhiên
        for _ in range(3):
            self.driver.execute_script(f"window.scrollBy(0, {random.randint(300, 800)})")
            ActionChains(self.driver).move_by_offset(random.randint(10,100), random.randint(10,100)).perform()
            time.sleep(random.uniform(0.5, 1.2))

    def _extract_reviews(self):
        try:
            #đợi trang shopee tải xong
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.shopee-product-rating"))
            )
            return [{
                #phần content chưa tìm được class --> chưa tìm ra giải pháp thay thế
                "content": el.find_element(By.CSS_SELECTOR, ".shopee-product-rating__main").text,
                "rating": el.find_element(By.CSS_SELECTOR, ".repeat-purchase-con").get_attribute("style"),
                "author": el.find_element(By.CSS_SELECTOR, ".shopee-product-rating__author-name").text,
                "date": el.find_element(By.CSS_SELECTOR, ".shopee-product-rating__time").text
            } for el in self.driver.find_elements(By.CSS_SELECTOR, "div.shopee-product-rating")]
        except Exception as e:
            print(f" Lỗi trích xuất: {str(e)}")
            return []

    def crawl(self, product_url):
        try:
            # Validate URL
            if not product_url.startswith(("http://", "https://")):
                product_url = f"https://{product_url}"
            
            self._start_stealth_browser()
            self.driver.get(product_url)
            
            # nếu như mà gặp captcha thì yêu cầu người dùng giải thủ công
            # VẤN ĐỀ: đã gặp CATPCHA nhưng đang bị phát hiện là bot, có nút thử lại nhưng không thể thử lại được
            if "verify" in self.driver.current_url:
                input("giải CAPTCHA thủ công và nhấn Enter...")
                self.driver.get(product_url)
            
            # mô phỏngg hành vi người dùng
            self._shopee_behavior()
            
            # xuất dữ liệu
            return self._extract_reviews()
            
        except Exception as e:
            print(f" Lỗi tổng: {str(e)}")
            return []
        finally:
            if self.driver:
                self.driver.quit()
            if self.profile_id:
                self.gen.stopProfile(self.profile_id)

if __name__ == "__main__":
    product_url = input("Nhập URL sản phẩm Shopee: ").strip()
    
    # Chạy crawler
    crawler = ShopeeCrawler()
    reviews = crawler.crawl(product_url)
    
    if reviews:
        pd.DataFrame(reviews).to_csv("shopee_reviews.csv", index=False)
        print(f"Crawl thành công {len(reviews)} đánh giá!")
    else:
        print("Không tìm thấy đánh giá nào!")