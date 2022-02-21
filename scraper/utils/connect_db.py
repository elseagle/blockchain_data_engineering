import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
try:
    DB_HOST = os.environ["DB_HOST"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    DB_USER = os.environ["DB_USER"]
    DB_NAME = os.environ["DB_NAME"]
    DB_PORT = os.environ["DB_PORT"]

except KeyError:
    print("One of the database parameters not found in .env")
    exit()


def connect():
    try:

        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )

        cur = conn.cursor()
        print("Connected to database")

    except (Exception, psycopg2.DatabaseError) as error:

        print("Error while connecting to postgres", error)

    return conn, cur
