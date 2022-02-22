import os
import csv
from pathlib import Path
from dotenv import load_dotenv
from scraper.rarity_tools.create_table.get_initial_data import get_initial_data
from scraper.rarity_tools.create_table.upload_initial_data import convert_to_tuple
from scraper.utils.connect_db import connect
from scraper.utils.creation_utils import insert_many, select_many_records

load_dotenv()
try:
    PROJECT_DIRECTORY = os.environ["PROJECT_DIRECTORY"]
except KeyError:
    print("PROJECT_DIRECTORY not found in .env")
    exit()


def upload_new_data(conn, cur):
    upcoming_nft_sales = get_initial_data()
    if len(upcoming_nft_sales) <= 0:
        print("there is no valid upcoming nft")
        return
    upcoming_nft_list = []
    for upcoming_nft_sale in upcoming_nft_sales:
        cur.execute(
            f"""
            SELECT
            max_items,
            price,
            price_text,
            currency,
            sale_date,
            pre_sale_date FROM rarity.upcoming_nft_sales WHERE LOWER(rarity_id)=LOWER('{upcoming_nft_sale["id"]}');
            """
        )
        upcoming_nft_tuple = cur.fetchone()
        if not upcoming_nft_tuple:
            print(f"{upcoming_nft_sale['id']} not in database")
            upcoming_nft_list.append(convert_to_tuple(upcoming_nft_sale))

    print(upcoming_nft_list)
    if len(upcoming_nft_list) <= 0:
        print("No new data to add to the database")
        return
    project_directory = Path(PROJECT_DIRECTORY)
    with open(
        Path(f"{project_directory}/scraper/CSV_data/upcoming_nft_sales.csv"),
        "a",
        encoding="utf-8",
    ) as csvfile:
        csvwriter = csv.writer(csvfile)
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
    upload_new_data(conn, cur)
    cur.close()
