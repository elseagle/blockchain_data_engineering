from utils.connect_db import connect


def create_tables(conn, cur):

    cur.execute(
        """
        CREATE SCHEMA IF NOT EXISTS coingecko;
        """
    )
    cur.execute(
        """
        DROP TABLE IF EXISTS
        coingecko.category, coingecko.currency, coingecko.currency_category, coingecko.currency_details
        CASCADE;
        """
    )
    conn.commit()

    cur.execute(
        """
       CREATE TABLE coingecko.category (
            id SERIAL PRIMARY KEY,
            category_name VARCHAR(255) NOT NULL UNIQUE,
            category_id VARCHAR(255) NOT NULL UNIQUE
        );
        """
    )
    cur.execute(
        """
       CREATE TABLE coingecko.currency (
            id SERIAL PRIMARY KEY,
            currency_name VARCHAR NOT NULL UNIQUE,
            coin_gecko_url VARCHAR NOT NULL
        );
        """
    )
    cur.execute(
        """
       CREATE TABLE coingecko.currency_category (
            category_id INTEGER NOT NULL,
            currency_id INTEGER NOT NULL,
            PRIMARY KEY (category_id , currency_id),
            FOREIGN KEY (category_id) REFERENCES coingecko.category (id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (currency_id) REFERENCES coingecko.currency (id) ON UPDATE CASCADE ON DELETE CASCADE
        );
        """
    )
    cur.execute(
        """
       CREATE TABLE coingecko.currency_details (
            id SERIAL PRIMARY KEY,
            currency_id INTEGER NOT NULL,
            FOREIGN KEY (currency_id) REFERENCES coingecko.currency (id) ON UPDATE CASCADE ON DELETE CASCADE,
            currency_name VARCHAR NOT NULL,
            check_date VARCHAR NOT NULL,
            time_of_check VARCHAR NOT NULL,
            coin_gecko_url VARCHAR NOT NULL,
            currency_website VARCHAR,
            currency_price VARCHAR NOT NULL,
            market_cap VARCHAR,
            trading_volume VARCHAR,
            market_cap_rank VARCHAR,
            all_time_high VARCHAR,
            all_time_low VARCHAR,
            one_day_low VARCHAR,
            one_day_high VARCHAR,
            seven_day_low VARCHAR,
            seven_day_high VARCHAR,
            archived BOOLEAN NOT NULL DEFAULT FALSE
        );
        """
    )
    conn.commit()
    print("tables created successfully")


if __name__ == "__main__":
    conn, cur = connect()
    create_tables(conn, cur)
    cur.close()
