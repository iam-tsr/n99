import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server.src.config.pg_config import get_db_connection

conn = get_db_connection()

try:
    if conn:
        with conn.cursor() as cur:
            # Fetch all rows from the user_data table
            cur.execute("SELECT * FROM user_data;")
            rows = cur.fetchall()

            print("\n--- User Data ---")
            for row in rows:
                print(
                    f"user_id: {row[0]}, movie_name: {row[1]}, event_date: {row[2]}, cinema_name: {row[3]}, track_id: {row[4]}"
                )
            print("--------------------\n")

except Exception as e:
    print("Connection failed.")
    print(e)