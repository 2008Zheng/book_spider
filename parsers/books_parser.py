from bs4 import BeautifulSoup

def parse_books(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("li.col-xs-6")

    results = []
    for item in items:
        title_tag = item.select_one("article.product_pod h3 a")
        title = title_tag.get("title", "").strip() if title_tag else ""

        price_tag = item.select_one("p.price_color")
        price = 0.0
        if price_tag:
            try:
                price = float(price_tag.text.replace("£", "").strip())
            except:
                pass

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
