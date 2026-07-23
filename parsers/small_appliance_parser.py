"""
小家电品类 · 通用解析器
适用：Cosori / Outin / 同类跨境 DTC 商品列表页
特点：价格多为 USD，需识别场景关键词（portable / pro / smart）
"""

from bs4 import BeautifulSoup
from typing import List, Dict
import re

# 场景关键词 → 标签（优先级从上到下）
SCENE_RULES = [
    ("travel",     ["travel", "便携", "出行", "camping"]),
    ("portable",   ["portable", "mini", "compact", "迷你", "口袋"]),
    ("smart",      ["smart", "wifi", "app", "智能", "物联网"]),
    ("pro",        ["pro", "professional", "商用", "专业"]),
    ("home",       ["home", "household", "家用", "桌面"]),
]

def detect_scene(title: str) -> str:
    t = title.lower()
    for tag, kws in SCENE_RULES:
        for kw in kws:
            if kw in t:
                return tag
    return "home"

def parse_price(raw: str) -> float:
    if not raw:
        return 0.0
    raw = raw.replace("Â", "").replace("£", "").replace("$", "").replace("€", "").replace(",", "").strip()
    try:
        return float(raw)
    except ValueError:
        return 0.0

def parse_small_appliance(html: str, site: str = "") -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = []

    # 通用商品卡片选择器（覆盖 Shopify/Astro/自定义主题）
    cards = soup.select("li.product, div.product-card, article.product")
    if not cards:
        # 兜底：抓所有带价格的链接
        cards = soup.select("a[href*='/products/']")

    for card in cards:
        title_tag = card.select_one("h2, h3, .product-title, .title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        price_tag = card.select_one(".price, .product-price, span.price")
        price = parse_price(price_tag.get_text(strip=True) if price_tag else "")

        # 货币判定
        raw_price = price_tag.get_text(strip=True) if price_tag else ""
        currency = "USD"
        if "£" in raw_price: currency = "GBP"
        elif "€" in raw_price: currency = "EUR"
        elif "$" in raw_price: currency = "USD"
        elif "¥" in raw_price or "元" in raw_price: currency = "CNY"

        scene = detect_scene(title)

        items.append({
            "sku": f"{site}_{len(items)+1}",
            "title": title,
            "price": price,
            "currency": currency,
            "scene_tag": scene,
            "rating": 0.0  # 列表页通常无评分，详情页可补
        })

    return items
