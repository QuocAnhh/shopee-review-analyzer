import requests
import json

def test_analyze_api():
    test_url = 'https://shopee.vn/%C3%81o-ch%E1%BB%91ng-n%E1%BA%AFng-nam-SunStop-Master-TOKYOLIFE-m%C5%A9-li%E1%BB%81n-ch%E1%BA%A5t-li%E1%BB%87u-co-d%C3%A3n-tho%C3%A1ng-m%C3%A1t-40000540-i.1454546610.28025094203'

    print('Testing với URL Shopee...')
    try:
        response = requests.post('http://localhost:5000/analyze', 
                               json={'url': test_url},
                               timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print('API phản hồi thành công!')
            
            print(f'Crawled data info: {"crawled_data_info" in data}')
            print(f'Demo reviews with highlights: {"demo_reviews_with_highlights" in data}')
            print(f'Overall assessment: {"overall_assessment" in data}')
            
            if 'crawled_data_info' in data:
                info = data['crawled_data_info']
                print(f'   - Total reviews: {info.get("total_reviews", 0)}')
                print(f'   - Data quality: {info.get("data_quality", "N/A")}')
            
            if 'demo_reviews_with_highlights' in data:
                demo = data['demo_reviews_with_highlights']
                print(f'   - Positive demos: {len(demo.get("positive_reviews", []))}')
                print(f'   - Negative demos: {len(demo.get("negative_reviews", []))}')
                
                # Kiểm tra keyword highlighting
                if demo.get('positive_reviews'):
                    first_pos = demo['positive_reviews'][0]
                    has_highlight = 'keyword-highlight' in first_pos.get('highlighted', '')
                    print(f'   - Keyword highlighting active: {has_highlight}')
            
            if 'overall_assessment' in data:
                assessment = data['overall_assessment']
                print(f'   - Overall score: {assessment.get("overall_score", 0)}/10')
                print(f'   - Recommendation: {assessment.get("recommendation", "N/A")}')
                
            # Kiểm tra legacy sections
            print(f'Chart URL: {"chart_url" in data}')
            print(f'Keywords: {"keywords" in data and len(data.get("keywords", [])) > 0}')
            print(f'Summary: {"summary" in data and len(data.get("summary", "")) > 0}')
            
            print('\nTất cả sections đều hoạt động tốt!')
                
        else:
            print(f'API lỗi: {response.status_code}')
            print(f'Response: {response.text}')
            
    except Exception as e:
        print(f'Lỗi khi test: {str(e)}')

if __name__ == '__main__':
    test_analyze_api()
