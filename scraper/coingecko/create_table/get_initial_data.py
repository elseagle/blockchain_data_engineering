import os
import time
import requests
import asyncio
import aiohttp
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from utils.user_agents import user_agents
from coingecko.async_get_coin_info import get_coins


def get_initial_data(number_of_coins=120):
    load_dotenv()

    try:
        PROXY_USERNAME = os.environ["PROXY_USERNAME"]
        PROXY_PASSWORD = os.environ["PROXY_PASSWORD"]
        PROJECT_DIRECTORY = os.environ["PROJECT_DIRECTORY"]
    except KeyError:
        print("Proxy username or proxy_password or PROJECT_DIRECTORY not found in .env")
        exit()

    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )  # windows only

    proxy = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@proxy.inv.tech:24000"
    start = time.time()
    user_agent = user_agents()
    headers = {
        "Alt-Used": "www.coingecko.com",
        "Host": "www.coingecko.com",
        "Referer": "https://www.coingecko.com/",
        "User-Agent": user_agent,
    }
    page = requests.get("https://www.coingecko.com/")
    soup = BeautifulSoup(page.content, "html.parser")
    project_directory = Path(PROJECT_DIRECTORY)
    with open(
        Path(f"{project_directory}/web_pages/coingecko.html"),
        "wb",
    ) as f:
        f.write(page.content)

    category_list = soup.find("ul", {"data-target": "searchable.itemList"})

    category_list = [
        (category.text, category["data-category-id"])
        for category in category_list.find_all("button")[1:]
    ]

    print(category_list, len(category_list))
    print("\n")

    pages = []

    coin_table = soup.find(
        "table", {"data-target": "gecko-table.table portfolios-v2.table"}
    ).find("tbody")

    async def get_page(session, url, limit):
        async with session.get(url, proxy=proxy, ssl=False) as resp:
            page = await resp.text()
            soup = BeautifulSoup(page, "html.parser")
            coin_table = soup.find(
                "table", {"data-target": "gecko-table.table portfolios-v2.table"}
            ).find("tbody")
            coin_rows.extend(coin_table.find_all("tr", limit=limit))

    async def get_pages(pages):
        async with aiohttp.ClientSession() as session:

            tasks = [
                asyncio.create_task(
                    get_page(
                        session, f"https://www.coingecko.com/?page={count+2}", limit
                    )
                )
                for count, limit in enumerate(pages)
            ]
            await asyncio.gather(*tasks)

    if number_of_coins <= 100:
        coin_rows = coin_table.find_all("tr", limit=number_of_coins)

    else:
        coin_rows = coin_table.find_all("tr", limit=100)
        number_of_coins = number_of_coins - 100
        pages = [100] * (number_of_coins // 100)
        if (number_of_coins % 100) > 0:
            pages.append(number_of_coins % 100)

        asyncio.run(get_pages(pages))

    print(pages)
    print("\n")

    currency_details = asyncio.run(get_coins(coin_rows))
    print(currency_details, len(currency_details))

    end = time.time()
    total_time = end - start
    print("\n")
    print(f"total scraping time is {total_time}")

    # with open(
    #     r"C:\Users\IndiAndInvi\Desktop\DESKTOP\SOGO\certik\blockchain_scraper\s.py", "w"
    # ) as f:
    #     f.write(str(currency_details))

    return currency_details, category_list

    # get all categories on first run and add to category table
    # get all coins on first run and do all necessary mapping
