import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server.src.config.pg_config import get_db_connection

conn = get_db_connection()

try:
    job_id = "f617b82b-9c64-435f-8f04-aa4bc6d23d8d"

    with conn.cursor() as cur:
        if cur.execute("SELECT * FROM user_data WHERE job_id = %s;", (job_id,)).fetchone():
            cur.execute("""
                DELETE FROM user_data
                WHERE job_id = %s;         
            """, (job_id,))
            conn.commit()
            print("Deleted user from user_data.")
        else:
            print(f"No user found with job_id {job_id} in user_data.")

except Exception as e:
    print("Connection failed.")
    print(e)