import aiohttp
from bs4 import BeautifulSoup

ASOS_URL = "https://www.asos.com/women/new-in/cat/?cid=27108"

async def fetch_asos_new_dresses(limit=20):
    async with aiohttp.ClientSession() as session:
        async with session.get(ASOS_URL) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    items = []

    for product in soup.select("article")[:limit]:
        title_tag = product.select_one("h2")
        link_tag = product.select_one("a")
        price_tag = product.select_one('[data-testid="productPrice"]')

        if title_tag and link_tag and price_tag:
            name = title_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            link = "https://www.asos.com" + link_tag.get("href", "")
            items.append((name, price, link))

    return items
