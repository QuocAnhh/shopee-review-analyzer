import scrapy
import json

class ShopeeSpider(scrapy.Spider):
    name = "shopee_reviews"
    allowed_domains = ["shopee.vn"]

    def start_requests(self):
        product_id = "20784854176"  
        shop_id = "173392916" 

        url = f"https://shopee.vn/api/v2/item/get_ratings?itemid={20784854176}&shopid={173392916}&limit=50&offset=0"
        yield scrapy.Request(url, callback=self.parse_reviews)
        

    def parse_reviews(self, response):
        data = json.loads(response.text)
        reviews = data.get("data", {}).get("ratings", [])
        print(response.text)


        for review in reviews:
            print("Username:", review.get("author_username"))
            print("Rating:", review.get("rating_star"))
            print("Comment:", review.get("comment"))
            print("Created at:", review.get("ctime"))
            yield {
                "username": review.get("author_username"),
                "rating": review.get("rating_star"),
                "comment": review.get("comment"),
                "created_at": review.get("ctime"),
            }

        offset = response.meta.get("offset", 0) + 50
        if len(reviews) > 0:
            next_url = f"https://shopee.vn/api/v2/item/get_ratings?itemid={20784854176}&shopid={173392916}&limit=50&offset={offset}"
            yield scrapy.Request(next_url, callback=self.parse_reviews, meta={"offset": offset})
