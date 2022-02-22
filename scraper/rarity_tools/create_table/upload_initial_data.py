import os
import csv
from pathlib import Path
from dotenv import load_dotenv
from create_table import create_table
from scraper.rarity_tools.create_table.get_initial_data import get_initial_data
from scraper.utils.connect_db import connect
from scraper.utils.creation_utils import insert_many, select_many_records

load_dotenv()
try:
    PROJECT_DIRECTORY = os.environ["PROJECT_DIRECTORY"]
except KeyError:
    print("PROJECT_DIRECTORY not found in .env")
    exit()


def convert_to_tuple(upcoming_nft_sale):
    project = (
        short_description
    ) = (
        max_items
    ) = (
        price
    ) = (
        price_text
    ) = currency = sale_date = pre_sale_date = website = discord_link = listed_date = ""
    if "Project" in upcoming_nft_sale:
        project = upcoming_nft_sale["Project"]

    if "Short Description" in upcoming_nft_sale:
        short_description = upcoming_nft_sale["Short Description"]
    else:
        if "Featured Description" in upcoming_nft_sale:
            short_description = upcoming_nft_sale["Featured Description"]

    if "Max Items" in upcoming_nft_sale:
        max_items = upcoming_nft_sale["Max Items"]

    if "Price" in upcoming_nft_sale:
        price = upcoming_nft_sale["Price"]

    if "Price Text" in upcoming_nft_sale:
        price_text = upcoming_nft_sale["Price Text"]

    if "Currency" in upcoming_nft_sale:
        currency = upcoming_nft_sale["Currency"]

    else:
        currency = "ETH"

    if "Sale Date" in upcoming_nft_sale:
        sale_date = upcoming_nft_sale["Sale Date"]

    else:
        sale_date = "To be Announced"

    if "Presale Date" in upcoming_nft_sale:
        pre_sale_date = upcoming_nft_sale["Presale Date"]

    if "Website" in upcoming_nft_sale:
        website = upcoming_nft_sale["Website"]

    if "Discord" in upcoming_nft_sale:
        discord_link = upcoming_nft_sale["Discord"]

    if "TwitterId" in upcoming_nft_sale:
        twitter_id = upcoming_nft_sale["TwitterId"]

    if "Listed Date" in upcoming_nft_sale:
        listed_date = upcoming_nft_sale["Listed Date"]
    return (
        upcoming_nft_sale["id"],
        project,
        short_description,
        max_items,
        price,
        price_text,
        currency,
        sale_date,
        pre_sale_date,
        website,
        discord_link,
        twitter_id,
        listed_date,
    )


def seed_table(conn, cur):
    upcoming_nft_sales = get_initial_data()
    if len(upcoming_nft_sales) <= 0:
        print("there is no valid upcoming nft")
        return
    create_table(conn, cur)
    upcoming_nft_list = []
    for upcoming_nft_sale in upcoming_nft_sales:
        upcoming_nft_list.append(convert_to_tuple(upcoming_nft_sale))

    print(upcoming_nft_list)
    project_directory = Path(PROJECT_DIRECTORY)
    with open(
        Path(f"{project_directory}/scraper/CSV_data/upcoming_nft_sales.csv"),
        "w",
        encoding="utf-8",
    ) as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(
            [
                "rarity_id",
                "project",
                "short_description",
                "max_items",
                "price",
                "price_text",
                "currency",
                "sale_date",
                "pre_sale_date",
                "website",
                "discord_link",
                "twitter_id",
                "listed_date",
            ]
        )
        csvwriter.writerows(upcoming_nft_list)
    insert_many(
        cur,
        upcoming_nft_list,
        f"""
        INSERT INTO rarity.upcoming_nft_sales(rarity_id,
            project,
            short_description,
            max_items,
            price,
            price_text,
            currency,
            sale_date,
            pre_sale_date,
            website,
            discord_link,
            twitter_id,
            listed_date
        ) VALUES 
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """,
        upcoming_nft_list,
    )

    conn.commit()
    select_many_records(cur, f"SELECT * FROM rarity.upcoming_nft_sales;")


if __name__ == "__main__":
    conn, cur = connect()
    seed_table(conn, cur)
    cur.close()
