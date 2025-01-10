import scrapy as sc
from ..items import YotpoextractItem
import os
import json

class YotpoExtractor(sc.Spider):
    name = "yotpo"

    def start_requests(self):
        input_file = r"D:\\python_scripts\\project\\Data_analytical\\Scrapy\\yotpoextract\\yotpoextract\\input.txt"
        try:
            with open(input_file, "r") as fh:
                lines = fh.readlines()
        except FileNotFoundError:
            self.logger.error("Input file not found: %s", input_file)
            return

        for line in lines:
            value = line.strip()
            if value:
                url = (
                    f"https://api-cdn.yotpo.com/v1/widget/fwAplI6cqaFLAdrUf9pbfDbDzfTMCEa8WSdUyDwM/"
                    f"products/{value}/reviews.json?per_page=150&sort=date&direction=desc&page=1"
                )
                yield sc.Request(url=url, callback=self.parse_reviews, meta={'product_id': value, 'page': 1})

    def parse_reviews(self, response):
        product_id = response.meta['product_id']
        page = response.meta['page']
        
        try:
            data = response.json()
        except ValueError:
            self.logger.error("Invalid JSON response received")
            return

        reviews = data.get("response", {}).get("reviews", [])
        if not reviews:
            self.logger.warning(f"No reviews found for product ID: {product_id} on page {page}")
            return

        review_items = []
        for review in reviews:
            item = YotpoextractItem()
            item["reviews_id"] = review.get("id", "N/A")
            item["review_content"] = review.get("content", "N/A")
            item["review_title"] = review.get("title", "N/A")
            item["review_date"] = review.get("created_at", "N/A")
            item["review_rating"] = review.get("score", "N/A")

            review_items.append(item)
            yield item

        if review_items:
            os.makedirs("output", exist_ok=True)
            jsonfilename = os.path.join("output", f"{product_id}_page_{page}.json")
            try:
                with open(jsonfilename, 'w', encoding='utf-8') as fh:
                    json.dump([dict(item) for item in review_items], fh, ensure_ascii=False, indent=4)
                self.logger.info(f"Saved reviews for product ID {product_id} on page {page} to {jsonfilename}")
            except Exception as e:
                self.logger.error(f"Error saving reviews for product ID {product_id} on page {page}: {e}")
        
        next_page = page + 1
        if len(reviews) == 150:  
            next_url = (
                f"https://api-cdn.yotpo.com/v1/widget/fwAplI6cqaFLAdrUf9pbfDbDzfTMCEa8WSdUyDwM/"
                f"products/{product_id}/reviews.json?per_page=150&sort=date&direction=desc&page={next_page}"
            )
            yield sc.Request(url=next_url, callback=self.parse_reviews, meta={'product_id': product_id, 'page': next_page})
        else:
            self.logger.info(f"Finished processing all reviews for product ID {product_id}.")
