# Configuration files to the database connection, environment variables, and other related settings.

import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conn_string = os.getenv("DATABASE_URL")

def get_db_connection():
    if conn_string:
        try:
            # Establish a connection to the PostgreSQL database
            conn = psycopg.connect(conn_string)
            print("Database connection established successfully.")
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None
    else:
        print("Warning: DATABASE_URL is not set in environment variables.")
        return None