# Userdata PostgreSQL operations

from src.config.db_config import get_db_connection
from loguru import logger

class DataPG:
    def __init__(self):
        self.conn = get_db_connection()

    def create_user_data(self, user_id, movie, date, cinema, job_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT job_id FROM user_data WHERE movie = %s AND date = %s AND cinema = %s;", (movie, date, cinema))
                existing_data = cur.fetchone()
                
                if existing_data:
                    ref_job_id = existing_data[0]
                    logger.info("User data already exists in user_data. Inserting data in to linked_data instead.")
                    cur.execute("""
                    INSERT INTO linked_data (user_id, job_id)
                    VALUES (%s, %s);
                    """, (user_id, ref_job_id))

                    self.conn.commit()
                    logger.info("Inserted user data into linked_data.")
                    return
                
                else:
                    cur.execute("""
                    INSERT INTO user_data (user_id, movie, date, cinema, job_id)
                    VALUES (%s, %s, %s, %s, %s);
                    """, (user_id, movie, date, cinema, job_id))

                    self.conn.commit()
                    logger.info("Inserted user data into user_data.")
                    return

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def read_user_data(self, job_id: str):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM user_data WHERE job_id = %s;", (job_id,))
                rows = cur.fetchall()
                logger.info(f"Fetched user data for job_id {job_id}")
                return rows

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def read_userID(self, job_id: str):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT user_id FROM linked_data WHERE job_id = %s;", (job_id,))
                linked_rows = cur.fetchall()

                cur.execute("SELECT user_id FROM user_data WHERE job_id = %s;", (job_id,))
                user_rows = cur.fetchall()

                user_ids = [row[0] for row in linked_rows] + [row[0] for row in user_rows]
                logger.info(f"Fetched user IDs for job_id {job_id}")
                return user_ids

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def find_job(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT date, movie, cinema, job_id FROM user_data;")
                rows = cur.fetchall()
                logger.info("Fetched all user data from user_data.")
                records = [
                    {"date": row[0].isoformat(), "movie": row[1], "cinema": row[2], "job_id": str(row[3])} for row in rows
                ]
                return records

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def update_user_data(self, job_id, movie, date, cinema):
        try:
            with self.conn.cursor() as cur:
                if cur.execute("SELECT * FROM user_data WHERE job_id = %s;", (job_id,)).fetchone():
                    cur.execute("""
                        UPDATE user_data
                        SET movie = %s, date = %s, cinema = %s
                        WHERE job_id = %s;
                    """, (movie, date, cinema, job_id))

                    self.conn.commit()
                    logger.info("Updated user data in user_data.")
                else:
                    logger.info(f"No user data found with job_id {job_id} in user_data.")

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def delete_user_data(self, job_id):
        try:
            with self.conn.cursor() as cur:
                if cur.execute("SELECT * FROM user_data WHERE job_id = %s;", (job_id,)).fetchone():
                    cur.execute("DELETE FROM user_data WHERE job_id = %s;", (job_id,))
                    self.conn.commit()
                    logger.info(f"Deleted user data for job_id {job_id} from user_data.")
                else:
                    logger.info(f"No user data found with job_id {job_id} in user_data.")

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def connection_close(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")



if __name__ == "__main__":
    data_pg = DataPG()
    # data_pg.create_user_data("22", "Hoppers", "2026-03-23", "Vegas Mall", str(uuid.uuid4()))
    # data = data_pg.read_user_data("17")
    # data = data_pg.find_job()
    user_ids = data_pg.read_linked_data("418c5201-189f-481b-96a7-63be90504674")
    # data = [data_pg.read_linked_data_by_user_id(user_id) for user_id in user_ids]
    # data_pg.update_user_data("17", "Updated Movie", "2026-03-23", "Updated Cinema")
    # data_pg.delete_user_data("17")
    print(user_ids)
    data_pg.connection_close()