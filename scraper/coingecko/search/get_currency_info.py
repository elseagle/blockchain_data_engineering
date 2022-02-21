import random
import requests
from utils.connect_db import connect
from utils.creation_utils import insert_item, insert_many, select_many_records
from get_coingecko_data import get_category_data, get_coin_data
from coingecko.currencies_and_categories.categories import categories
from coingecko.currencies_and_categories.currencies import currencies


def process_currency_details(currency_details):
    currency_category_list = []
    currency_details_list = []
    for currency in currency_details:
        if type(currency) != dict:
            continue
        cur.execute(
            f"""
            SELECT id , currency_id FROM coingecko.currency_details WHERE LOWER(currency_name)=LOWER('{currency["currency_name"]}');
            """
        )
        currency_details_tuple = cur.fetchone()
        if currency_details_tuple:
            currency_details_id = currency_details_tuple[0]
            currency_id = currency_details_tuple[1]
            print(f"{currency_details_id} for {currency['currency_name']}")
            cur.execute(
                """ UPDATE coingecko.currency_details
                    SET archived = TRUE
                    WHERE id = %s""",
                (currency_details_id,),
            )
            conn.commit()
        else:
            cur.execute(
                f"""
                    SELECT id FROM coingecko.currency WHERE LOWER(currency_name)=LOWER('{currency["currency_name"]}');
                    """
            )
            currency_tuple = cur.fetchone()
            if not currency_tuple:
                insert_item(
                    cur,
                    currency["currency_name"],
                    f"""
                INSERT INTO coingecko.currency(currency_name, coin_gecko_url) VALUES 
                (%s,%s) RETURNING id;
                """,
                    (currency["currency_name"], currency["coin_gecko_url"]),
                )
                currency_tuple = cur.fetchone()
            currency_id = currency_tuple[0]

        currency_details_list.append(
            (
                currency_id,
                currency["currency_name"],
                currency["check_date"],
                currency["time_of_check"],
                currency["coin_gecko_url"],
                currency["currency_website"],
                currency["currency_price"],
                currency["market_cap"],
                currency["trading_volume"],
                currency["market_cap_rank"],
                currency["all_time_high"],
                currency["all_time_low"],
                currency["one_day_low"],
                currency["one_day_high"],
                currency["seven_day_low"],
                currency["seven_day_high"],
            )
        )
        for category in currency["currency_categories"]:
            cur.execute(
                f"""
                SELECT id FROM coingecko.category WHERE LOWER(category_name)=LOWER('{category}');
                """
            )

            category_tuple = cur.fetchone()
            if not category_tuple:
                print("category not found in database")
                continue
            category_id = category_tuple[0]
            print(f"this is category_id {category_id} for {currency_id}")
            cur.execute(
                f"""
                SELECT category_id, currency_id FROM coingecko.currency_category 
                WHERE (category_id=%s AND currency_id=%s) ;
                """,
                (category_id, currency_id),
            )
            if not cur.fetchone():
                currency_category_list.append((category_id, currency_id))

    print("\n")
    insert_many(
        cur,
        currency_category_list,
        f"""
        INSERT INTO coingecko.currency_category(category_id, currency_id) VALUES 
        (%s,%s);
        """,
        currency_category_list,
    )
    print("currency_category manytomany data upload successful")

    insert_many(
        cur,
        currency_details_list,
        f"""
        INSERT INTO coingecko.currency_details(currency_id, currency_name, check_date, time_of_check,
        coin_gecko_url, currency_website, currency_price, market_cap, trading_volume, market_cap_rank,
        all_time_high, all_time_low,one_day_low, one_day_high, seven_day_low, seven_day_high   
        ) VALUES 
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """,
        currency_details_list,
    )

    conn.commit()

    print("All data uploaded successfully")


def get_coin_info(conn, cur, currency):
    cur.execute(
        f"""
            SELECT coin_gecko_url FROM coingecko.currency WHERE LOWER(currency_name)=LOWER('{currency}');
            """
    )
    currency_tuple = cur.fetchone()
    if not currency_tuple:
        print(f"{currency} not found in database")
        res = requests.get(f"https://api.coingecko.com/api/v3/search?query={currency}")
        if res.status_code != 200:
            print(f"Error making request to coingecko api for {currency}")
            return

        if len(res.json()["coins"]) <= 0:
            print(f"Coin with NAME {currency} DOES NOT exist in coingecko")
            return
        coin_gecko_id = res.json()["coins"][0]["id"]
        insert_item(
            cur,
            currency,
            f"""
        INSERT INTO coingecko.currency(currency_name, coin_gecko_url) VALUES 
        (%s,%s) RETURNING coin_gecko_url;
        """,
            (currency, f"https://www.coingecko.com/en/coins/{coin_gecko_id}"),
        )
        currency_tuple = cur.fetchone()
        conn.commit()
    coin_gecko_url = currency_tuple[0]
    print(coin_gecko_url)
    currency_details = get_coin_data(currency, coin_gecko_url)
    process_currency_details(currency_details)


def get_category_info(conn, cur, category, number_of_coins):
    if category == "All":
        category_id = "All"
    else:
        cur.execute(
            f"""
            SELECT category_id FROM coingecko.category WHERE LOWER(category_name)=LOWER('{category["name"]}');
            """
        )
        category_tuple = cur.fetchone()
        if not category_tuple:
            print("category not found in database")
            insert_item(
                cur,
                category["name"],
                f"""
            INSERT INTO coingecko.category(category_name, category_id) VALUES 
            (%s, %s) RETURNING id;
            """,
                (category["name"], category["category_id"]),
            )
            category_tuple = cur.fetchone()
            conn.commit()
        category_id = category_tuple[0]
        print(f"this is category_id {category_id}")
    currency_details = get_category_data(category_id, number_of_coins)
    process_currency_details(currency_details)


if __name__ == "__main__":

    category = random.choice(categories)
    currency = random.choice(currencies)
    number_of_coins = 5
    conn, cur = connect()
    get_category_info(conn, cur, category, number_of_coins)
    get_coin_info(conn, cur, currency)
    select_many_records(cur, f"SELECT * FROM coingecko.category;")
    select_many_records(cur, f"SELECT * FROM coingecko.currency;")
    select_many_records(cur, f"SELECT * FROM coingecko.currency_category;")
    select_many_records(cur, f"SELECT * FROM coingecko.currency_details;")
    cur.close()
