"""
户外对讲机品类 · 通用解析器
适用：Garmin / Baofeng / Motorola 类公开页
特点：圈层小众，场景以 hiking/cycling/emergency 为主
"""

from bs4 import BeautifulSoup
from typing import List, Dict
import re

SCENE_RULES = [
    ("ham",        ["ham", "业余", "uv-5r", "ht", "yaesu"]),
    ("gmrs",       ["gmrs", "frs", "中继", "repeater"]),
    ("hunting",    ["hunting", "狩猎", "隐蔽", "camouflage", "camo"]),
    ("cycling",    ["cycling", "骑行", "自行车", "bike"]),
    ("hiking",     ["hiking", "trekking", "登山", "徒步", "mountain"]),
    ("camping",    ["camping", "露营", "篝火", "outdoor"]),
    ("emergency",  ["emergency", "应急", "灾害", " preparedness"]),
]

def detect_scene(title: str) -> str:
    t = title.lower()
    for tag, kws in SCENE_RULES:
        for kw in kws:
            if kw in t:
                return tag
    return "outdoor"

def parse_price(raw: str) -> float:
    if not raw:
        return 0.0
    raw = raw.replace("Â", "").replace("£", "").replace("$", "").replace("€", "").replace(",", "").strip()
    try:
        return float(raw)
    except ValueError:
        return 0.0

def parse_walkie_talkie(html: str, site: str = "") -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = []

    cards = soup.select("li.product, div.product-card, article.product, .product-item")
    if not cards:
        cards = soup.select("a[href*='/products/'], a[href*='/p/'], a[href*='/shop/']")

    for card in cards:
        title_tag = card.select_one("h2, h3, .product-title, .title, .name")
        title = title_tag.get_text(strip=True) if title_tag else ""

        price_tag = card.select_one(".price, .product-price, span.price")
        price = parse_price(price_tag.get_text(strip=True) if price_tag else "")

        raw_price = price_tag.get_text(strip=True) if price_tag else ""
        currency = "USD"
        if "£" in raw_price: currency = "GBP"
        elif "€" in raw_price: currency = "EUR"
        elif "$" in raw_price: currency = "USD"

        # 对讲机常见功率/距离信息（作为副标题）
        sub_tag = card.select_one(".subtitle, .desc, .description")
        subtitle = sub_tag.get_text(strip=True).lower() if sub_tag else ""

        scene = detect_scene(title + " " + subtitle)

        items.append({
            "sku": f"{site}_{len(items)+1}",
            "title": title,
            "price": price,
            "currency": currency,
            "scene_tag": scene,
            "rating": 0.0
        })

    return items
