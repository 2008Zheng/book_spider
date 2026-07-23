"""
户外防晒用品品类 · 通用解析器
适用：迪卡侬 / 哥伦比亚 / 蕉下 类公开页
特点：山系溢价明显（蕉下 vs 迪卡侬），UPF50+ 是核心卖点
"""

from bs4 import BeautifulSoup
from typing import List, Dict
import re

SCENE_RULES = [
    ("uv",         ["upf50", "upf 50", "uv protection", "防紫外线", "紫外线"]),
    ("mountain",   ["mountain", "山系", "登山", "hiking", "越野"]),
    ("fishing",    ["fishing", "垂钓", "涉水", "kayak"]),
    ("running",    ["running", "马拉松", "jogging", "跑步"]),
    ("bucket",     ["bucket", "渔夫帽", "wide brim"]),
    ("kids",       ["kids", "儿童", "junior", "boy", "girl"]),
    ("daily",      ["daily", "通勤", "city", "urban", "休闲"]),
]

def detect_scene(title: str) -> str:
    t = title.lower()
    for tag, kws in SCENE_RULES:
        for kw in kws:
            if kw in t:
                return tag
    return "daily"

def parse_price(raw: str) -> float:
    if not raw:
        return 0.0
    raw = raw.replace("Â", "").replace("£", "").replace("$", "").replace("€", "").replace("¥", "").replace("元", "").replace(",", "").strip()
    try:
        return float(raw)
    except ValueError:
        return 0.0

def parse_sun_protect(html: str, site: str = "") -> List[Dict]:
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
        currency = "CNY"  # 默认人民币，后面按符号修正
        if "£" in raw_price: currency = "GBP"
        elif "€" in raw_price: currency = "EUR"
        elif "$" in raw_price: currency = "USD"
        elif "¥" in raw_price or "元" in raw_price: currency = "CNY"

        scene = detect_scene(title)

        # UPF 标签提取（用于后续筛选）
        upf = ""
        upf_tag = card.select_one(".badge, .tag, .label")
        if upf_tag and "upf" in upf_tag.get_text(strip=True).lower():
            upf = upf_tag.get_text(strip=True)

        items.append({
            "sku": f"{site}_{len(items)+1}",
            "title": title,
            "price": price,
            "currency": currency,
            "scene_tag": scene,
            "rating": 0.0,
            "upf": upf
        })

    return items
