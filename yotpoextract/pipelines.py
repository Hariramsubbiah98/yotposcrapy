import sqlite3
import logging

class YotpoextractPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("Reviews.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS Yotpo_table(
                Review_Id INTEGER PRIMARY KEY,
                Review_text TEXT NOT NULL,
                Review_title TEXT,
                Review_date TEXT,
                Review_rating INTEGER 
            )""")
        self.conn.commit()
        logging.info("Table 'Yotpo_table' is ready.")

    def process_item(self, review_items, spider):
        self.store_db(review_items)
        return review_items

    def store_db(self, item):
        logging.info(f"Inserting item into DB: {item}")
        self.curr.execute("""
            INSERT INTO Yotpo_table (Review_Id, Review_text, Review_title, Review_date, Review_rating) 
            VALUES (?, ?, ?, ?, ?)
            """, (
                item["reviews_id"], 
                item["review_content"],
                item["review_title"], 
                item["review_date"], 
                item["review_rating"]
            ))
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
