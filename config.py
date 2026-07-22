from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class SiteConfig:
    name: str                    # 站点名称
    base_url: str               # 基础 URL
    page_url_template: str       # 分页 URL 模板（用 {page} 占位）
    total_pages: int = 1        # 总页数
    first_page_is_root: bool = True  # 第一页是否用根路径
    delay: float = 1.0         # 请求间隔（秒）
    output_file: str = ""       # 输出 CSV 路径
    model_fields: List[str] = field(default_factory=list)  # CSV 表头


# 图书站点配置
BOOKS_CONFIG = SiteConfig(
    name="books",
    base_url="https://books.toscrape.com",
    page_url_template="/catalogue/page-{page}.html",
    total_pages=50,
    first_page_is_root=True,
    delay=1.0,
    output_file="data/books.csv",
    model_fields=[
        "platform", "item_id", "title", "author",
        "publisher", "price", "original_price",
        "comment_count", "rating", "crawl_time"
    ]
)

# 名言站点配置
QUOTES_CONFIG = SiteConfig(
    name="quotes",
    base_url="https://quotes.toscrape.com",
    page_url_template="/page/{page}/",
    total_pages=10,
    first_page_is_root=True,
    delay=1.0,
    output_file="data/quotes.csv",
    model_fields=["text", "author", "tags", "crawl_time"]
)
