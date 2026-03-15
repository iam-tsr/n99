import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server.src.config.pg_config import get_db_connection

conn = get_db_connection()

try:
    if conn:
        with conn.cursor() as cur:
            data_to_insert =[
                ("TSR", "tsr@outlook.com", "Dhurander 2", "2026-03-18", "Vegas Mall"),
                ("Ansh", "ansh@outlook.com", "Inception", "2026-03-19", "Cinema City"),
                ("Harshit", "harshit@outlook.com", "The Matrix", "2026-03-20", "Cineplex")
            ]
            # Fetch all rows from the user_data table
            cur.executemany("""
                WITH inserted_user AS (
                    INSERT INTO user_profile (username, email)
                    VALUES (%s, %s)
                    RETURNING user_id
                )
                INSERT INTO user_data (user_id, movie, date, cinema)
                SELECT user_id, %s, %s, %s FROM inserted_user;
            """, data_to_insert)

            conn.commit()
            print("Inserted new user into user_profile.")

except Exception as e:
    print("Connection failed.")
    print(e)