# Userprofile PostgreSQL operations

from server.src.config.pg_config import get_db_connection

class ProfilePG:
    def __init__(self):
        self.conn = get_db_connection()

    def create_user_profile(self, username, email, movie, date, cinema):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                WITH inserted_user AS (
                    INSERT INTO user_profile (username, email)
                    VALUES (%s, %s)
                    RETURNING user_id
                )
                INSERT INTO user_data (user_id, movie, date, cinema)
                SELECT user_id, %s, %s, %s FROM inserted_user;
                """, (username, email, movie, date, cinema))

                self.conn.commit()
                print("Inserted user into user_profile.")

        except Exception as e:
            print("Connection failed.")
            print(e)

    def read_user_profiles(self, user_id: str):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM user_profile WHERE user_id = %s;", (user_id,))
                rows = cur.fetchall()
                print(f"Fetched user profiles for user_id {user_id}")
                return rows

        except Exception as e:
            print("Connection failed.")
            print(e)

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
                    print("Updated user in user_profile.")
                else:
                    print(f"No user found with user_id {user_id} in user_profile.")

        except Exception as e:
            print("Connection failed.")
            print(e)

    def delete_user_profile(self, user_id):
        try:
            with self.conn.cursor() as cur:
                if cur.execute("SELECT * FROM user_profile WHERE user_id = %s;", (user_id,)).fetchone():
                    cur.execute("""
                        DELETE FROM user_profile
                        WHERE user_id = %s;         
                    """, (user_id,))
                    self.conn.commit()
                    print("Deleted user from user_profile.")
                else:
                    print(f"No user found with user_id {user_id} in user_profile.")

        except Exception as e:
            print("Connection failed.")
            print(e)

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    profile_pg = ProfilePG()

    # Example usage
    data = profile_pg.read_user_profiles("17")
    print(data)