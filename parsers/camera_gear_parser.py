"""
摄影器材品类 · 通用解析器
适用：SmallRig / Neewer / B&H 类商品列表页
特点：价格带宽（20–800 USD），场景以 studio/vlog/travel 为主
"""

from bs4 import BeautifulSoup
from typing import List, Dict
import re

SCENE_RULES = [
    ("wireless",   ["wireless", "无线", "bluetooth"]),
    ("studio",     ["studio", "棚拍", "softbox", "影棚"]),
    ("vlog",       ["vlog", "selfie", "直播", "直播补光"]),
    ("ring",       ["ring", "环形", "美颜"]),
    ("travel",     ["travel", "轻量", "碳纤维", "carbon", "便携"]),
    ("macro",      ["macro", "微距", "特写"]),
]

def detect_scene(title: str) -> str:
    t = title.lower()
    for tag, kws in SCENE_RULES:
        for kw in kws:
            if kw in t:
                return tag
    return "studio"

def parse_price(raw: str) -> float:
    if not raw:
        return 0.0
    raw = raw.replace("Â", "").replace("£", "").replace("$", "").replace("€", "").replace(",", "").strip()
    try:
        return float(raw)
    except ValueError:
        return 0.0

def parse_camera_gear(html: str, site: str = "") -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = []

    cards = soup.select("li.product, div.product-card, article.product, .product-item")
    if not cards:
        cards = soup.select("a[href*='/products/'], a[href*='/p/']")

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
        elif "¥" in raw_price: currency = "CNY"

        # 评分（部分站点有）
        rating_tag = card.select_one(".rating, .stars, .star-rating")
        rating = 0.0
        if rating_tag:
            m = re.search(r"(\d+\.?\d*)", rating_tag.get_text())
            if m: rating = float(m.group(1))

        scene = detect_scene(title)

        items.append({
            "sku": f"{site}_{len(items)+1}",
            "title": title,
            "price": price,
            "currency": currency,
            "scene_tag": scene,
            "rating": rating
        })

    return items
