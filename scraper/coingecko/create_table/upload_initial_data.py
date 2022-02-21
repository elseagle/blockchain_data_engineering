from create_tables import create_tables
from get_initial_data import get_initial_data
from utils.connect_db import connect
from utils.creation_utils import insert_item, insert_many, select_many_records


def seed_tables(conn, cur, number_of_coins):
    currency_details, category_list = get_initial_data(
        number_of_coins
    )  # download web page and save csv too
    create_tables(conn, cur)
    print("uploading initial data")
    insert_many(
        cur,
        category_list,
        f"""
        INSERT INTO coingecko.category(category_name, category_id) VALUES 
        (%s, %s);
        """,
        category_list,
    )
    print("category data upload successful")

    currency_category_list = []
    currency_details_list = []
    for currency in currency_details:
        if type(currency) != dict:
            continue
        insert_item(
            cur,
            currency["currency_name"],
            f"""
            INSERT INTO coingecko.currency(currency_name, coin_gecko_url) VALUES 
            (%s,%s) RETURNING id;
            """,
            (currency["currency_name"], currency["coin_gecko_url"]),
        )
        currency_id = cur.fetchone()[0]
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
            category_id = cur.fetchone()[0]
            print(f"this is category_id {category_id} for {currency_id}")
            if category_id:
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
    select_many_records(cur, f"SELECT * FROM coingecko.category;")
    select_many_records(cur, f"SELECT * FROM coingecko.currency;")
    select_many_records(cur, f"SELECT * FROM coingecko.currency_category;")
    select_many_records(cur, f"SELECT * FROM coingecko.currency_details;")


if __name__ == "__main__":
    conn, cur = connect()
    seed_tables(conn, cur, 130)
    cur.close()
