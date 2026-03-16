from config.pg_config import get_db_connection

def create_tables():
    """
    Create the users and servers tables in the database.
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email_id VARCHAR(255) UNIQUE NOT NULL,
            user_name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS servers (
            id SERIAL PRIMARY KEY,
            movie_search_alerted BOOLEAN DEFAULT FALSE
        )
        """
    )
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            conn.commit()
            print("Tables created successfully.")
            cur.close()
        except Exception as e:
            print(f"Error creating tables: {e}")
            conn.rollback()
        finally:
            conn.close()
    else:
        print("Could not connect to database. Please check your DATABASE_URL in .env")

if __name__ == '__main__':
    create_tables()
