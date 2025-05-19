import requests
import os
from pathlib import Path
import time
import re
from datetime import datetime
import pandas as pd

def extract_ids_from_url(url):
    """trích xuất shop_id và item_id từ URL sản phẩm"""
    pattern = r'i\.(\d+)\.(\d+)'
    match = re.search(pattern, url)
    
    if match:
        shop_id = int(match.group(1))
        item_id = int(match.group(2))
        return shop_id, item_id
    
    raise ValueError("Không thể trích xuất shop_id và item_id từ URL này")

def get_reviews(shop_id, user_id=None, limit=50, offset=0):
    """lấy reviews từ api, trả về dữ liệu JSON"""
    url = "https://shopee.vn/api/v4/seller_operation/get_shop_ratings_new"
    
    params = {
        "limit": limit,
        "offset": offset,
        "shopid": shop_id
    }
    
    # optional 
    if user_id:
        params["userid"] = user_id
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        "Referer": "https://shopee.vn/"
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

def transform_reviews(reviews):
    """Chuyển đổi dữ liệu reviews thành định dạng chuẩn"""
    transformed_data = []
    for item in reviews:
        transformed_data.append({
            'rating': item.get('rating_star', ''),
            'comment': item.get('comment', '').replace('\n', ' '),
            'author': item.get('author_username', ''),
            'date': item.get('ctime', '')
        })
    return transformed_data

def save_reviews(reviews, output_path, format_type='xlsx'):
    """Lưu reviews vào file theo định dạng được chọn (xlsx hoặc txt)"""
    if not reviews:
        print("Không có dữ liệu để lưu")
        return False
    
    try:
        if format_type.lower() == 'xlsx':
            df = pd.DataFrame(reviews)
            df.to_excel(output_path, index=False)
        elif format_type.lower() == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                for item in reviews:
                    f.write(f"Đánh giá: {item['rating']} sao\n")
                    f.write(f"Người đánh giá: {item['author']}\n")
                    f.write(f"Ngày: {item['date']}\n")
                    f.write(f"Nội dung: {item['comment']}\n")
                    f.write("-" * 80 + "\n")
        else:
            print(f"Định dạng {format_type} không được hỗ trợ. Hỗ trợ: xlsx, txt")
            return False
            
        print(f"Đã lưu {len(reviews)} đánh giá vào: {output_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi lưu file: {str(e)}")
        return False

def crawl_all_reviews(shop_id, item_id=None, limit_per_request=50, delay=1):
    """
    Crawl tất cả reviews có thể từ shop, trả về dữ liệu và trạng thái
    
    Args:
        shop_id: ID của shop
        item_id: ID của sản phẩm (để đặt tên file, không ảnh hưởng tới API)
        limit_per_request: Số lượng reviews mỗi lần gọi API
        delay: Thời gian chờ giữa các lần gọi API (giây)
        
    Returns:
        dict: Kết quả với keys: success, message, data, total_reviews, total_pages
    """
    try:
        result = {
            "success": False,
            "message": "",
            "data": [],
            "total_reviews": 0,
            "total_pages": 0
        }
        
        offset = 0
        current_page = 1
        all_reviews = []
        
        while True:
            try:
                print(f"Đang lấy trang {current_page} (offset {offset})...")
                response_json = get_reviews(shop_id, limit=limit_per_request, offset=offset)
                
                if "data" not in response_json:
                    message = f"Cấu trúc API không như mong đợi. Keys: {list(response_json.keys())}"
                    print(message)
                    result["message"] = message
                    break
                
                data = response_json.get("data", {})
                items = data.get("items", [])
                
                if not items:
                    print("Không còn đánh giá nào.")
                    break
                
                transformed_items = transform_reviews(items)
                all_reviews.extend(transformed_items)
                
                print(f"Đã lấy thêm {len(items)} đánh giá.")
                
                offset += limit_per_request
                current_page += 1
                
                if delay > 0:
                    print(f"Đợi {delay} giây trước khi lấy trang tiếp theo...")
                    time.sleep(delay)
                
            except Exception as e:
                error_message = f"Lỗi khi lấy đánh giá: {type(e).__name__}: {str(e)}"
                print(error_message)
                result["message"] = error_message
                break

        # Cập nhật kết quả
        actual_pages = current_page - 1
        print(f"Hoàn thành! Đã lấy tổng cộng {len(all_reviews)} đánh giá ({actual_pages} trang).")
        
        result["success"] = True
        result["data"] = all_reviews
        result["total_reviews"] = len(all_reviews)
        result["total_pages"] = actual_pages
        result["message"] = "Crawl thành công"
        
        return result
    
    except Exception as e:
        error_message = f"Lỗi không xác định: {type(e).__name__}: {str(e)}"
        print(error_message)
        return {
            "success": False,
            "message": error_message,
            "data": [],
            "total_reviews": 0,
            "total_pages": 0
        }

def main():
    """Hàm chính cho chế độ dòng lệnh"""
    # Thư mục đầu ra
    output_dir = Path(r"C:/download")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Lấy URL sản phẩm từ người dùng
    product_url = input("Nhập URL sản phẩm Shopee: ")
    
    # Chọn định dạng đầu ra
    format_type = input("Chọn định dạng file (xlsx/txt, mặc định xlsx): ").lower() or "xlsx"
    if format_type not in ["xlsx", "txt"]:
        print(f"Định dạng {format_type} không được hỗ trợ. Dùng mặc định: xlsx")
        format_type = "xlsx"
    
    try:
        # Lấy shop_id và item_id từ URL
        shop_id, item_id = extract_ids_from_url(product_url)
        print(f"Đã lấy: Shop ID = {shop_id}, Item ID = {item_id}")

        # Đặt tên file dựa trên item_id và timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"reviews_item_{item_id}_{timestamp}.{format_type}"
        output_path = output_dir / output_file
        
        print(f"Bắt đầu crawl tất cả đánh giá có thể. Bấm Ctrl+C để dừng.")
        result = crawl_all_reviews(shop_id, item_id)
        
        if result["success"] and result["data"]:
            save_reviews(result["data"], output_path, format_type)
            print(f"Lưu thành công vào {output_path}")
        else:
            print(f"Không thể lấy đánh giá: {result['message']}")
        
    except ValueError as e:
        print(f"Lỗi: {str(e)}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi API: {type(e).__name__}: {str(e)}")
    except Exception as e:
        print(f"Lỗi không xác định: {type(e).__name__}: {str(e)}")
    except KeyboardInterrupt:
        print("\nNgười dùng đã dừng quá trình crawl.")

# API function example
def get_product_reviews_api(product_url, format_type="json"):
    """
    Hàm ví dụ để tích hợp vào API
    
    Args:
        product_url: URL sản phẩm Shopee
        format_type: Định dạng trả về (json/xlsx/txt)
        
    Returns:
        dict: Kết quả với trạng thái và dữ liệu
    """
    try:
        shop_id, item_id = extract_ids_from_url(product_url)
        result = crawl_all_reviews(shop_id, item_id, delay=0.5)
        
        if format_type == "json":
            return result
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_file = Path(f"temp_reviews_{item_id}_{timestamp}.{format_type}")
            
            if save_reviews(result["data"], temp_file, format_type):
                result["file_path"] = str(temp_file)
            
            return result
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": []
        }

if __name__ == "__main__":
    main()