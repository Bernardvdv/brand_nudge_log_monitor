import psycopg2
import os


def create_db_con():
    connection = psycopg2.connect(
            host=os.getenv("HOST_AWS"),
            database=os.getenv("DB_AWS"),
            user=os.getenv("USERNAME_AWS"),
            password=os.getenv("PASSWORD_AWS"),
            port=os.getenv("PORT_AWS"),
            sslmode="disable"
        )
    return connection.cursor()
