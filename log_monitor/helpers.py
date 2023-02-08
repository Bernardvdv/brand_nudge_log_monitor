import psycopg2
import os


def create_db_con():
    connection = psycopg2.connect(
            host=os.getenv("HOST"),
            database=os.getenv("DB"),
            user=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            port=os.getenv("PORT"),
            sslmode="disable"
        )
    return connection.cursor()
