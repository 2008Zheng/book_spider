from spiders.base import BaseSpider
from config import BOOKS_CONFIG
from parsers.books_parser import parse_books
from models import Product
from typing import Dict


class BooksSpider(BaseSpider):
    """图书爬虫——继承通用框架"""

    def __init__(self):
        super().__init__(BOOKS_CONFIG)

    def parse(self, html: str) -> list[Dict]:
        return parse_books(html)

    def create_model(self, item: Dict) -> Product:
        return Product(
            platform="toscrape",
            item_id=item.get("item_id", ""),
            title=item.get("title", ""),
            author=item.get("author", ""),
            publisher=item.get("publisher", ""),
            price=item.get("price", 0.0),
            original_price=item.get("original_price", 0.0),
            comment_count=item.get("comment_count", 0),
            rating=item.get("rating", 0.0)
        )
