from spiders.books_spider import BooksSpider
from storage_sqlite import init_db, save_products
import logging

logging.basicConfig(level=logging.INFO)
init_db()
spider = BooksSpider()
items = spider.run()
save_products("books", items)
