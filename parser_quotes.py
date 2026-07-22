from bs4 import BeautifulSoup

def parse_quotes_page(html):
    soup = BeautifulSoup(html, "html.parser")

    # 每条名言在 div.quote 里
    items = soup.select("div.quote")
    print(f"[DEBUG] 找到 {len(items)} 个 div.quote 标签")

    results = []
    for item in items:
        # 名言内容（span.text）
        text_tag = item.select_one("span.text")
        text = text_tag.get_text(strip=True) if text_tag else ""

        # 作者（small.author）
        author_tag = item.select_one("small.author")
        author = author_tag.get_text(strip=True) if author_tag else ""

        # 标签（div.tags a.tag）
        tags = [t.get_text(strip=True) for t in item.select("div.tags a.tag")]

        results.append({
            "text": text,
            "author": author,
            "tags": ", ".join(tags)
        })

    return results
