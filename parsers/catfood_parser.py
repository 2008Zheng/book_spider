from bs4 import BeautifulSoup
from typing import List, Dict

def parse_catfood(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div.product-card")
    results = []
    for item in items:
        title = item.select_one("h2").get_text(strip=True)
        price = item.select_one(".price").get_text(strip=True).replace("$", "")
        results.append({
            "item_id": title[:50],
            "title": title,
            "price": float(price) if price else 0.0,
            "rating": 0.0
        })
    return results
