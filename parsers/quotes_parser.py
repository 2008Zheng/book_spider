from bs4 import BeautifulSoup

def parse_quotes(html: str) -> list[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div.quote")

    results = []
    for item in items:
        text_tag = item.select_one("span.text")
        text = text_tag.get_text(strip=True) if text_tag else ""

        author_tag = item.select_one("small.author")
        author = author_tag.get_text(strip=True) if author_tag else ""

        tags = [t.get_text(strip=True) for t in item.select("div.tags a.tag")]

        results.append({
            "text": text,
            "author": author,
            "tags": ", ".join(tags)
        })

    return results
