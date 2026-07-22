from spiders.base import BaseSpider
from config import QUOTES_CONFIG
from parsers.quotes_parser import parse_quotes
from models import Quote

class QuotesSpider(BaseSpider):
    """名言爬虫——继承通用框架"""

    def __init__(self):
        super().__init__(QUOTES_CONFIG)

    def parse(self, html: str) -> list[Dict]:
        return parse_quotes(html)

    def create_model(self, item: Dict) -> Quote:
        return Quote(
            text=item.get("text", ""),
            author=item.get("author", ""),
            tags=item.get("tags", "")
        )
