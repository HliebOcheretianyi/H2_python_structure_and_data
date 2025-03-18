import psycopg2

import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE", "")
USER = os.getenv("USER", "")
PASSWORD = os.getenv("PASSWORD", "")
HOST = os.getenv("HOST", "")
PORT = os.getenv("PORT", "")

try:
    connection = psycopg2.connect(
        database = DATABASE,
        user = USER,
        password = PASSWORD,
        host = HOST,
        port = HOST
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        pass

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL:", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")


