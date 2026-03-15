import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server.src.config.pg_config import get_db_connection

conn = get_db_connection()

try:
    job_id = "aed61330-0c76-4626-b0fd-44c2337300e5"
    
    with conn.cursor() as cur:
        if cur.execute("SELECT * FROM user_data WHERE job_id = %s;", (job_id,)).fetchone():
            cur.execute("""
                UPDATE user_data
                SET movie = %s, date = %s, cinema = %s
                WHERE job_id = %s;
            """, ("Updated Movie", "2026-03-23", "Updated Cinema", job_id))
            conn.commit()
            print("Updated user in user_data.")
        else:
            print(f"No user found with job_id {job_id} in user_data.")

except Exception as e:
    print("Connection failed.")
    print(e)