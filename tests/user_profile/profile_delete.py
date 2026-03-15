import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server.src.config.pg_config import get_db_connection

conn = get_db_connection()

try:
    user_id = 19

    with conn.cursor() as cur:
        if cur.execute("SELECT * FROM user_profile WHERE user_id = %s;", (user_id,)).fetchone():
            cur.execute("""
                DELETE FROM user_profile
                WHERE user_id = %s;         
            """, (user_id,))
            conn.commit()
            print("Deleted user from user_profile.")
        else:
            print(f"No user found with user_id {user_id} in user_profile.")

except Exception as e:
    print("Connection failed.")
    print(e)