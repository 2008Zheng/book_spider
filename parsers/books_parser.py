from bs4 import BeautifulSoup
from typing import List, Dict
import re

def parse_books(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("li.col-xs-6")
    results = []

    for item in items:
        # 书名
        title_tag = item.select_one("article.product_pod h3 a")
        title = ""
        if title_tag:
            title = title_tag.get("title", "").strip() or title_tag.get_text(strip=True)

        # 价格
        price_tag = item.select_one("p.price_color")
        price = 0.0
        if price_tag:
            raw = price_tag.get_text(strip=True)
            # 去掉 £ 和可能的乱码字符
            raw = raw.replace("£", "").replace("Â", "").replace(",", "").strip()
            try:
                price = float(raw)
            except ValueError:
                price = 0.0

        # 评分
        rating_tag = item.select_one("p.star-rating")
        rating = 0.0
        if rating_tag:
            cls = rating_tag.get("class", [])
            if len(cls) >= 2:
                rating_map = {
                    "One": 1.0, "Two": 2.0, "Three": 3.0,
                    "Four": 4.0, "Five": 5.0
                }
                rating = rating_map.get(cls[1], 0.0)

        results.append({
            "item_id": title,
            "title": title,
            "author": "",
            "publisher": "",
            "price": price,
            "original_price": 0.0,
            "comment_count": 0,
            "rating": rating
        })

    return results
