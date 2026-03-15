from config.pg_config import SessionLocal
from model.db.models import MovieAlert, User

def check_db():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total Users: {len(users)}")
        for u in users:
            print(f"  - {u.email}")

        alerts = db.query(MovieAlert).all()
        print(f"Total Alerts: {len(alerts)}")
        for a in alerts:
            print(f"  - ID: {a.id}, User: {a.user.email}, Movie: {a.movie_name}, Target Date: {a.target_date}, Fulfilled: {a.is_fulfilled}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
