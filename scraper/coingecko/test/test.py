from scraper.utils.connect_db import connect

conn, cur = connect()
cur.execute(
    f"""
            SELECT * FROM coingecko.category;
            """
)
print(cur.fetchone())

cur.close()
