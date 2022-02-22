from scraper.utils.connect_db import connect


def create_table(conn, cur):
    cur.execute(
        """
        CREATE SCHEMA IF NOT EXISTS rarity;
        """
    )
    cur.execute(
        """
        DROP TABLE IF EXISTS
        rarity.upcoming_nft_sales
        CASCADE;
        """
    )
    conn.commit()

    cur.execute(
        """
       CREATE TABLE rarity.upcoming_nft_sales (
            id SERIAL PRIMARY KEY,
            rarity_id VARCHAR(255) NOT NULL UNIQUE,
            project VARCHAR(255),
            short_description VARCHAR(255),
            max_items VARCHAR(255),
            price VARCHAR(255),
            price_text VARCHAR(255),
            currency VARCHAR(255),
            sale_date VARCHAR(255),
            pre_sale_date VARCHAR(255),
            website VARCHAR(255),
            discord_link VARCHAR(255),
            twitter_id VARCHAR(255),
            listed_date VARCHAR(255)
        );
        """
    )
    conn.commit()
    print("upcoming_nft_sales table created susccessfully ")


if __name__ == "__main__":
    conn, cur = connect()
    create_table(conn, cur)
    cur.close()
