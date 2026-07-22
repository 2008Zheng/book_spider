from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Product:
    platform: str = ""
    item_id: str = ""
    title: str = ""
    author: str = ""
    publisher: str = ""
    price: float = 0.0
    original_price: float = 0.0
    comment_count: int = 0
    rating: float = 0.0
    crawl_time: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "platform": self.platform,
            "item_id": self.item_id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "price": self.price,
            "original_price": self.original_price,
            "comment_count": self.comment_count,
            "rating": self.rating,
            "crawl_time": self.crawl_time
        }


@dataclass
class Quote:
    text: str = ""
    author: str = ""
    tags: str = ""
    crawl_time: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "text": self.text,
            "author": self.author,
            "tags": self.tags,
            "crawl_time": self.crawl_time
        }
