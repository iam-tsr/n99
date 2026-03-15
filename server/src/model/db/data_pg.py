# Userdata PostgreSQL operations

from server.src.config.pg_config import get_db_connection

class DataPG:
    def __init__(self):
        self.conn = get_db_connection()

    def create_user_data(self, user_id, movie, date, cinema):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                INSERT INTO user_data (user_id, movie, date, cinema)
                VALUES (%s, %s, %s, %s);
                """, (user_id, movie, date, cinema))

                self.conn.commit()
                print("Inserted user data into user_data.")

        except Exception as e:
            print("Connection failed.")
            print(e)

    def read_user_data(self, user_id: str):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM user_data WHERE user_id = %s;", (user_id,))
                rows = cur.fetchall()
                print(f"Fetched user data for user_id {user_id}")
                return rows

        except Exception as e:
            print("Connection failed.")
            print(e)

    def update_user_data(self, user_id, movie, date, cinema):
        try:
            with self.conn.cursor() as cur:
                if cur.execute("SELECT * FROM user_data WHERE user_id = %s;", (user_id,)).fetchone():
                    cur.execute("""
                        UPDATE user_data
                        SET movie = %s, date = %s, cinema = %s
                        WHERE user_id = %s;
                    """, (movie, date, cinema, user_id))

                    self.conn.commit()
                    print("Updated user data in user_data.")
                else:
                    print(f"No user data found with user_id {user_id} in user_data.")

        except Exception as e:
            print("Connection failed.")
            print(e)

    def delete_user_data(self, user_id):
        try:
            with self.conn.cursor() as cur:
                if cur.execute("SELECT * FROM user_data WHERE user_id = %s;", (user_id,)).fetchone():
                    cur.execute("DELETE FROM user_data WHERE user_id = %s;", (user_id,))
                    self.conn.commit()
                    print(f"Deleted user data for user_id {user_id} from user_data.")
                else:
                    print(f"No user data found with user_id {user_id} in user_data.")

        except Exception as e:
            print("Connection failed.")
            print(e)

    def connection_close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")



if __name__ == "__main__":
    data_pg = DataPG()
    # data_pg.create_user_data("17", "Hoppers", "2026-03-23", "Vegas Mall")
    data = data_pg.read_user_data("17")
    print(data)
    # data_pg.update_user_data("17", "Updated Movie", "2026-03-23", "Updated Cinema")
    # data_pg.delete_user_data("17")
    data_pg.connection_close()