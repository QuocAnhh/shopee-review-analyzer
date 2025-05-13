import time
import random
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from Genlogin import Genlogin
import re

def inject_anti_bot_scripts(driver):
    # Xóa navigator.webdriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """
    })
    # Fake plugin length
    driver.execute_script("""
    Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
    """)
    driver.execute_script("""
    Object.defineProperty(navigator, 'languages', {get: () => ['vi-VN', 'en-US']});
    """)

def simulate_human_behavior(driver):
    for _ in range(random.randint(5, 10)):
        driver.execute_script(f"window.scrollBy(0, {random.randint(100, 600)})")
        time.sleep(random.uniform(0.5, 1.8))
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, 'a, button')
            if elements:
                ActionChains(driver).move_to_element(random.choice(elements)).perform()
                time.sleep(random.uniform(0.3, 1.2))
        except: pass

def get_cookies_from_genlogin(profile_id):
    gen = Genlogin("")
    run_data = gen.runProfile(profile_id)
    if not run_data.get("wsEndpoint"):
        raise Exception("Không thể khởi chạy profile")
    debugger_address = run_data["wsEndpoint"].replace("ws://", "").split("/")[0]

    options = Options()
    options.add_experimental_option("debuggerAddress", debugger_address)
    service = Service('crawl/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    inject_anti_bot_scripts(driver)

    driver.get("https://shopee.vn/")
    print("Đăng nhập shopee và thao tác qua như người thật để tránh bị detect là bot")
    input("Sau khi login & thao tác đủ, nhấn Enter để tiếp tục...")
    simulate_human_behavior(driver)
    cookies = driver.get_cookies()
    driver.quit()
    gen.stopProfile(profile_id)
    cookie_dict = {c['name']: c['value'] for c in cookies}
    return cookie_dict

def crawl_reviews_api(shop_id, item_id, cookie_dict, max_review=200):
    headers = {
        "user-agent": "Mozilla/5.0",
        "referer": f"https://shopee.vn/product/{shop_id}/{item_id}",
        "cookie": "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])
    }
    all_reviews = []
    offset = 0
    limit = 50
    while len(all_reviews) < max_review:
        url = f"https://shopee.vn/api/v2/item/get_ratings?itemid={item_id}&shopid={shop_id}&limit={limit}&offset={offset}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Lỗi hoặc bị block tại offset {offset}: {resp.text[:200]}")
            break
        data = resp.json()
        ratings = data.get("data", {}).get("ratings", [])
        if not ratings:
            break
        all_reviews.extend(ratings)
        print(f"Đã lấy {len(all_reviews)} review...")
        offset += limit
        time.sleep(2 + (offset % 7))  # delay tránh bị block
    return all_reviews

def extract_simple_reviews(raw_reviews):
    reviews = []
    for r in raw_reviews:
        reviews.append({
            "rating": r.get("rating_star"),
            "username": r.get("author_username"),
            "comment": r.get("comment"),
            "date": r.get("ctime"),
            "images": ",".join(r.get("images", [])) if r.get("images") else ""
        })
    return reviews

if __name__ == "__main__":
    # Hiển thị danh sách profile để chọn
    gen = Genlogin("")
    profiles = gen.getProfiles(0, 10).get("profiles", [])
    if not profiles:
        print("Không có profile nào trong Genlogin.")
        exit(1)
    print("Danh sách profile:")
    for i, profile in enumerate(profiles):
        print(f"{i+1}. {profile.get('profileName') or profile.get('title') or profile.get('name') or 'NoName'} (id: {profile.get('id') or profile.get('profile_id')})")
    while True:
        idx_input = input("Nhập số thứ tự profile muốn sử dụng: ").strip()
        if idx_input.isdigit() and 1 <= int(idx_input) <= len(profiles):
            idx = int(idx_input) - 1
            break
        else:
            print("Vui lòng nhập số hợp lệ trong danh sách.")
    profile_id = profiles[idx].get('id') or profiles[idx].get('profile_id')

    # Lấy cookie từ profile Genlogin
    cookie_dict = get_cookies_from_genlogin(profile_id)

    product_url = input("Nhập link sản phẩm Shopee: ").strip()
    # xử lý link sản phẩm
    m = re.search(r'/product/(\d+)/(\d+)', product_url)
    if m:
        shop_id, item_id = m.group(1), m.group(2)
    else:
        shop_id = input("Nhập shop_id: ").strip()
        item_id = input("Nhập item_id: ").strip()
    while True:
        max_review_input = input("Số lượng review muốn lấy tối đa (mặc định 200): ").strip()
        if not max_review_input:
            max_review = 200
            break
        if max_review_input.isdigit():
            max_review = int(max_review_input)
            break
        else:
            print("Vui lòng nhập số nguyên hợp lệ hoặc để trống.")
    
    # gọi API
    raw_reviews = crawl_reviews_api(shop_id, item_id, cookie_dict, max_review=max_review)
    reviews = extract_simple_reviews(raw_reviews)
    if reviews:
        df = pd.DataFrame(reviews)
        df.to_csv("shopee_reviews.csv", index=False)
        print(f"Đã lưu {len(reviews)} review vào file shopee_reviews.csv")
    else:
        print("Không lấy được review nào hoặc bị block.")