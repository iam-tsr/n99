# Userprofile PostgreSQL operations

from src.config.db_config import get_db_connection

from loguru import logger

class ProfilePG:
    def __init__(self):
        self.conn = get_db_connection()

    def create_user_profile(self, username, email):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT user_id FROM user_profile WHERE email = %s;", (email,))
                existing_user = cur.fetchone()
                if existing_user:
                    logger.info(f"User with email {email} already exists in user_profile with user_id {existing_user[0]}.")
                    return existing_user[0]
        
                cur.execute("""
                INSERT INTO user_profile (username, email)
                VALUES (%s, %s)
                RETURNING user_id
                """, (username, email))
                
                returned_id = cur.fetchone()[0]
                self.conn.commit()
                logger.info(f"Inserted user with user_id {returned_id} into user_profile.")
                return returned_id

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def read_user_profiles(self, user_id: str):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM user_profile WHERE user_id = %s;", (user_id,))
                count = cur.fetchone()[0]
                return count

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def read_user_data(self, user_id: str):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT username, email FROM user_profile WHERE user_id = %s;", (user_id,))
                rows = cur.fetchall()
                logger.info(f"Fetched linked data for user_id {user_id}")
                return rows

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def update_user_profile(self, user_id, username, email):
        try:
            with self.conn.cursor() as cur:
                if cur.execute("SELECT * FROM user_profile WHERE user_id = %s;", (user_id,)).fetchone():
                    cur.execute("""
                        UPDATE user_profile
                        SET username = %s, email = %s
                        WHERE user_id = %s;
                    """, (username, email, user_id))

                    self.conn.commit()
                    logger.info(f"Updated user with user_id {user_id} in user_profile.")
                else:
                    logger.info(f"No user found with user_id {user_id} in user_profile.")

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def delete_user_profile(self, user_id):
        try:
            with self.conn.cursor() as cur:
                if cur.execute("SELECT * FROM user_profile WHERE user_id = %s;", (user_id,)).fetchone():
                    cur.execute("""
                        DELETE FROM user_profile
                        WHERE user_id = %s;         
                    """, (user_id,))
                    self.conn.commit()
                    logger.info(f"Deleted user with user_id {user_id} from user_profile.")
                else:
                    logger.info(f"No user found with user_id {user_id} in user_profile.")

        except Exception as e:
            logger.error(f"Connection failed. Error: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")


if __name__ == "__main__":
    profile_pg = ProfilePG()

    # Example usage
    # data = profile_pg.read_user_profiles("17")
    # print(data)

    # insert_data = profile_pg.create_user_profile("TSR", "tushar@outlook.com")
    data = profile_pg.read_user_data("17")
    print(data)