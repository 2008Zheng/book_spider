from bs4 import BeautifulSoup

def parse_list_page(html):
    soup = BeautifulSoup(html, "html.parser")

    # books.toscrape：每本书在一个 li 里
    items = soup.select("li.col-xs-6")
    print(f"[DEBUG] 找到 {len(items)} 个 li.col-xs-6 标签")

    results = []
    for item in items:
        # ✅ 书名：只取 title 属性，不碰 get_text()
        title_tag = item.select_one("article.product_pod h3 a")
        title = title_tag.get("title", "").strip() if title_tag else ""

        # 价格
        price_tag = item.select_one("p.price_color")
        price = 0.0
        if price_tag:
            try:
                price = float(price_tag.text.replace("£", "").strip())
            except:
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

        # 库存状态
        stock_tag = item.select_one("p.instock.availability")
        in_stock = stock_tag.get_text(strip=True) if stock_tag else ""

        results.append({
            "item_id": title,
            "title": title,          # ✅ 只保留干净的 title 属性
            "author": "",
            "publisher": "",
            "price": price,
            "rating": rating,
            "comment_count": 0,
            "in_stock": in_stock
        })

    return results
