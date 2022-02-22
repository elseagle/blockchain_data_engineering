import requests
import time
import asyncio
from bs4 import BeautifulSoup
from scraper.coingecko.async_get_coin_info import get_coins


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # windows only


def get_coin_data(currency_name, coin_gecko_url):
    currency_details = asyncio.run(get_coins([(currency_name, coin_gecko_url)]))
    print(currency_details, len(currency_details))
    return currency_details


def get_category_data(category_id, number_of_coins):
    # check if more pages for when number_of_coins > 100
    start = time.time()
    if category_id == "All":
        url = f"https://www.coingecko.com/"
    else:
        url = f"https://www.coingecko.com/en/categories/{category_id}"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    try:
        coin_table = soup.find(
            "table", {"data-target": "gecko-table.table portfolios-v2.table"}
        ).find("tbody")
    except:
        print(f"This category {category_id} does not have any coins")
        return []

    coin_rows = coin_table.find_all("tr", limit=number_of_coins)
    currency_details = asyncio.run(get_coins(coin_rows))
    print(currency_details, len(currency_details))
    end = time.time()
    total_time = end - start
    print("\n")
    print(f"total scraping time is {total_time}")
    return currency_details
