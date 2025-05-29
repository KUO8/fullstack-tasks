import time
import psycopg2
import os

while True:
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        conn.close()
        print("Database is ready!")
        break
    except psycopg2.OperationalError:
        print("Waiting for database to be ready...")
        time.sleep(1)
