# PostgreSQL operations
from config.pg_config import get_db_connection

def execute_query(query, params=None):
    """
    Execute a query that doesn't return data (INSERT, UPDATE, DELETE).
    """
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
            return True
        except Exception as e:
            print(f"Error executing query: {e}")
            conn.rollback()
        finally:
            conn.close()
    return False

def fetch_all(query, params=None):
    """
    Execute a query and fetch all results.
    """
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            conn.close()
    return None

# User Operations
def register_user(email_id, user_name):
    """
    Registers a new user in the users table.
    """
    query = "INSERT INTO users (email_id, user_name) VALUES (%s, %s) ON CONFLICT (email_id) DO NOTHING"
    return execute_query(query, (email_id, user_name))

def get_user_by_email(email_id):
    """
    Fetches user details by email.
    """
    query = "SELECT * FROM users WHERE email_id = %s"
    return fetch_one(query, (email_id,))

# Server Operations
def set_movie_alert_status(server_id, alerted):
    """
    Updates the movie_search_alerted status for a server.
    """
    query = "INSERT INTO servers (id, movie_search_alerted) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET movie_search_alerted = EXCLUDED.movie_search_alerted"
    return execute_query(query, (server_id, alerted))

def get_server_alert_status(server_id):
    """
    Fetches the alert status for a server.
    """
    query = "SELECT movie_search_alerted FROM servers WHERE id = %s"
    return fetch_one(query, (server_id,))

def fetch_one(query, params=None):
    """
    Execute a query and fetch one result.
    """
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchone()
        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            conn.close()
    return None