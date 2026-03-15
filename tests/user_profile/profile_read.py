import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server.src.config.pg_config import get_db_connection

conn = get_db_connection()

try:
    if conn:
        with conn.cursor() as cur:
            # Fetch all rows from the user_profile table
            cur.execute("SELECT * FROM user_profile;")
            rows = cur.fetchall()

            print("\n--- User Profiles ---")
            for row in rows:
                print(
                    f"user_id: {row[0]}, username: {row[1]}, email: {row[2]}, created_at: {row[3]}"
                )
            print("--------------------\n")

except Exception as e:
    print("Connection failed.")
    print(e)