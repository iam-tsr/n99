import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# We need the user to provide their Neon database URL in the .env file.
# E.g., postgresql://username:password@ep-crimson-sun-xyz.ap-southeast-1.aws.neon.tech/dbname?sslmode=require
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Warning: DATABASE_URL is not set in environment variables.")
    # You could optionally raise an exception here depending on your app's needs
    # raise Exception("DATABASE_URL environment variable is not set")

if DATABASE_URL:
    # SQLAlchemy requires postgresql:// instead of postgres:// for some dialects
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
else:
    engine = None
    SessionLocal = None
    Base = declarative_base()

    def get_db():
        raise NotImplementedError("Database is not configured properly.")