import psycopg2

from decouple import config

def db_connection():
    con=psycopg2.connect(
            host=config('PG_HOST'),
            user=config('PG_USER'),
            password=config('PG_PASSWORD'),
            database=config('PG_DB')
        )
    return con
    