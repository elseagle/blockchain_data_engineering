import os
import csv
import asyncio
import aiofiles
import aiohttp
import pytz
from pathlib import Path
from datetime import datetime as dt
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from aiocsv import AsyncDictWriter
from scraper.utils.utils import remove_whitespace
from scraper.utils.user_agents import user_agents

load_dotenv()

PROXY_URL = os.getenv("PROXY_URL")
try:
    PROJECT_DIRECTORY = os.environ["PROJECT_DIRECTORY"]
except KeyError:
    print("PROJECT_DIRECTORY not found in .env")
    exit()


user_agent = user_agents()
headers = {
    "Alt-Used": "www.coingecko.com",
    "Host": "www.coingecko.com",
    "Referer": "https://www.coingecko.com/",
    "User-Agent": user_agent,
}
proxy = PROXY_URL


async def get_coin_info(session, coin_row, semaphore_):
    async with semaphore_:  # semaphore limits num of simultaneous downloads
        try:
            if type(coin_row) == tuple:
                currency_name, coin_gecko_url = coin_row
            else:
                coin_ = coin_row.find("td", class_="coin-name")
                currency_name = coin_["data-sort"]
                coin_gecko_url = f'https://www.coingecko.com{coin_.find("a")["href"]}'
            now = dt.now(tz=pytz.utc)
            check_date = now.strftime("%Y-%m-%d")
            time_of_check = now.strftime("%H:%M:%S")
            async with session.get(
                coin_gecko_url, proxy=proxy, headers=headers, ssl=False
            ) as resp:
                sub_page = await resp.text()
                sub_soup = BeautifulSoup(sub_page, "html.parser")
                coin_info = sub_soup.find(
                    "div", {"data-target": "coins-information.mobileOptionalInfo"}
                )

                currency_website, currency_categories = "", []
                try:
                    info_rows = coin_info.find_all("div", class_="coin-link-row")
                except Exception as e:
                    raise Exception(e)
                for info_row in info_rows:

                    info_title = info_row.find("span")
                    if not info_title:
                        continue
                    if "Website" in info_title:
                        currency_website = info_row.find("a")["href"]

                    elif "Tags" in info_title:
                        currency_categories = [
                            category.text for category in info_row.find_all("a")
                        ]

                coin_statistics = (
                    sub_soup.find("div", id="general")
                    .find("div", {"itemtype": "https://schema.org/Table"})
                    .find_all("tr")
                )

                currency_price = (
                    market_cap
                ) = (
                    market_cap_rank
                ) = (
                    all_time_high
                ) = (
                    all_time_low
                ) = one_day_low = one_day_high = seven_day_low = seven_day_high = ""

                for stat in coin_statistics:
                    stat_header = remove_whitespace(stat.find("th").text)
                    stat_text = remove_whitespace(stat.find("td").text)
                    if f"{currency_name} Price" in stat_header:
                        currency_price = stat_text

                    elif stat_header.lower() == "market cap":
                        market_cap = stat_text

                    elif "Trading Volume" in stat_header:
                        trading_volume = stat_text

                    elif (
                        "Market" in stat_header
                        and "Cap" in stat_header
                        and "Rank" in stat_header
                    ):
                        market_cap_rank = stat_text

                    elif "24h Low" in stat_header and "24h High" in stat_header:
                        one_day_prices = (
                            stat.find("td")
                            .find("span")
                            .find_all("span", {"data-target": "price.price"})
                        )
                        one_day_low = remove_whitespace(one_day_prices[0].text)
                        one_day_high = remove_whitespace(one_day_prices[1].text)

                    elif "7d Low" in stat_header and "7d High" in stat_header:
                        seven_day_prices = (
                            stat.find("td")
                            .find("span")
                            .find_all("span", {"data-target": "price.price"})
                        )
                        seven_day_low = remove_whitespace(seven_day_prices[0].text)
                        seven_day_high = remove_whitespace(seven_day_prices[1].text)

                    elif "All-Time High" in stat_header:
                        all_time_high = remove_whitespace(
                            stat.find("td")
                            .find("span")
                            .find("span", {"data-target": "price.price"})
                            .text
                        )

                    elif "All-Time Low" in stat_header:
                        all_time_low = remove_whitespace(
                            stat.find("td")
                            .find("span")
                            .find("span", {"data-target": "price.price"})
                            .text
                        )

                print(currency_name, coin_gecko_url)
                # print(currency_website)
                # print(currency_categories)
                # print(
                #     check_date,
                #     time_of_check,
                #     currency_price,
                #     market_cap,
                #     trading_volume,
                #     market_cap_rank,
                #     all_time_high,
                #     all_time_low,
                #     one_day_low,
                #     one_day_high,
                #     seven_day_low,
                #     seven_day_high,
                # )
                # print("\n")
                return {
                    "check_date": check_date,
                    "time_of_check": time_of_check,
                    "currency_name": currency_name,
                    "coin_gecko_url": coin_gecko_url,
                    "currency_website": currency_website,
                    "currency_categories": currency_categories,
                    "currency_price": currency_price,
                    "market_cap": market_cap,
                    "trading_volume": trading_volume,
                    "market_cap_rank": market_cap_rank,
                    "all_time_high": all_time_high,
                    "all_time_low": all_time_low,
                    "one_day_low": one_day_low,
                    "one_day_high": one_day_high,
                    "seven_day_low": seven_day_low,
                    "seven_day_high": seven_day_high,
                }

        except aiohttp.client_exceptions.ClientOSError as e:
            return await get_coin_info(session, coin_row, semaphore_)
        except aiohttp.client_exceptions.ServerDisconnectedError as e:
            return await get_coin_info(session, coin_row, semaphore_)

        except Exception as e:
            print(e)
            return e


async def get_coins(coin_rows):

    semaphore_ = asyncio.Semaphore(350)
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(get_coin_info(session, coin_row, semaphore_))
            for coin_row in coin_rows
        ]
        responses = await asyncio.gather(*tasks)

    project_directory = Path(PROJECT_DIRECTORY)
    async with aiofiles.open(
        Path(f"{project_directory}/scraper/CSV_data/coingecko.csv"),
        mode="a",
        encoding="utf-8",
        newline="",
    ) as afp:
        writer = AsyncDictWriter(
            afp,
            [
                "check_date",
                "time_of_check",
                "currency_name",
                "coin_gecko_url",
                "currency_website",
                "currency_categories",
                "currency_price",
                "market_cap",
                "trading_volume",
                "market_cap_rank",
                "all_time_high",
                "all_time_low",
                "one_day_low",
                "one_day_high",
                "seven_day_low",
                "seven_day_high",
            ],
            restval="NULL",
            quoting=csv.QUOTE_ALL,
        )
        await writer.writeheader()
        await writer.writerows(list(filter(lambda x: type(x) == dict, responses)))

    return responses
