import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server.src.config.pg_config import get_db_connection

conn = get_db_connection()

try:
    if conn:
        with conn.cursor() as cur:
            data_to_insert =[
                # ("17", "Hoppers", "2026-03-23", "Vegas Mall"),
                ("19", "Hoopers", "2026-03-23", "Vegas Mall"),
            ]
            cur.executemany("""
                INSERT INTO user_data (user_id, movie, date, cinema)
                VALUES (%s, %s, %s, %s)
            """, data_to_insert)

            conn.commit()
            print("Inserted new user into user_profile.")

except Exception as e:
    print("Connection failed.")
    print(e)