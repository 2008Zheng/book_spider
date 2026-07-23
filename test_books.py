import requests
from bs4 import BeautifulSoup

for i in [1, 2, 3]:
    url = f"https://books.toscrape.com/catalogue/page-{i}.html"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    prices = soup.select("li.col-xs-6 p.price_color")
    print(f"Page {i}: status={r.status_code}, books={len(prices)}, "
          f"sample={prices[0].get_text(strip=True) if prices else 'NONE'}")
