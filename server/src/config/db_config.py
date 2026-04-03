# Configuration files to the database connection, environment variables, and other related settings.

import os
import psycopg
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

conn_string = os.getenv("DATABASE_URL")

def get_db_connection():
    if conn_string:
        try:
            conn = psycopg.connect(conn_string, sslmode="require")
            return conn
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            return None
    else:
        logger.warning("Warning: DATABASE_URL is not set in environment variables.")
        return None