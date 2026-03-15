from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from loguru import logger

from config.pg_config import SessionLocal
from model.db.models import MovieAlert
from services.email_service import send_notification_email
from model.core.showing_spider import movies_showing

def check_movie_availability():
    """
    The main background task that checks if monitored movies are available.
    It runs every 6 hours.
    """
    logger.info("Agent Scheduler: Starting movie availability check...")
    db: Session = SessionLocal()
    if not db:
        logger.error("Agent Scheduler: DB not initialized.")
        return

    try:
        # Get all unfulfilled alerts
        active_alerts = db.query(MovieAlert).filter(MovieAlert.is_fulfilled == False).all()
        logger.info(f"Agent Scheduler: Found {len(active_alerts)} active alerts.")

        for alert in active_alerts:
            # Parse the target date
            try:
                target_dt = datetime.strptime(alert.target_date, "%Y-%m-%d").date()
            except ValueError:
                logger.error(f"Invalid date format for alert {alert.id}: {alert.target_date}")
                continue

            # Check if the target date is within the next 3 days
            current_date = datetime.now().date()
            if current_date <= target_dt <= current_date + timedelta(days=3):
                import json
                import os
                
                # Load cinema list mapping
                cinema_data = []
                parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                cinema_list_path = os.path.join(parent_dir, "cinema-list.json")
                if os.path.exists(cinema_list_path):
                    with open(cinema_list_path, "r") as f:
                        cinema_data = json.load(f).get("cinema", [])

                # Try to find a matching cinema slug/code (Improved fuzzy matching)
                cinema_slug = alert.cinema_place.strip()
                cinema_code = ""
                city_slug = "national-capital-region-ncr" # default if not found
                
                alert_words = set(alert.cinema_place.lower().split())
                for c in cinema_data:
                    cinema_words = set(c['name'].lower().replace("-", " ").split())
                    # Check if any significant word matches
                    if alert_words.intersection(cinema_words):
                        cinema_slug = c['name']
                        cinema_code = c['code']
                        city_slug = c['city']
                        break
                
                # Format date for BookMyShow (YYYYMMDD)
                bms_date = alert.target_date.replace("-", "")

                try:
                    logger.info(f"Agent Scheduler: Scrapping {cinema_slug} for {alert.movie_name} on {bms_date}")
                    # Scrape for this cinema
                    results = movies_showing(name=cinema_slug, code=cinema_code, city=city_slug, date=bms_date)
                    
                    # Check if the movie name exists (Improved word-based matching)
                    found = False
                    movie_keywords = set(alert.movie_name.lower().split())
                    for movie_title in results:
                        title_words = set(movie_title.lower().replace(":", " ").replace("-", " ").split())
                        # Check if at least 2 words or 50% of keywords match
                        matches = movie_keywords.intersection(title_words)
                        if len(matches) >= min(len(movie_keywords), 2):
                            found = True
                            break

                    if found:
                        logger.info(f"Agent Scheduler: Tickets found for '{alert.movie_name}' at {cinema_slug}!")
                        
                        email_sent = send_notification_email(
                            to_email=alert.user.email,
                            movie_name=alert.movie_name,
                            cinema_place=alert.cinema_place,
                            target_date=alert.target_date
                        )
                        
                        alert.is_fulfilled = True
                        db.commit()
                        logger.info(f"Agent Scheduler: Marked alert {alert.id} as fulfilled.")
                    else:
                        logger.info(f"Agent Scheduler: No tickets yet for '{alert.movie_name}' at {cinema_slug}.")
                except Exception as scraper_err:
                    logger.error(f"Agent Scheduler: Scraper failed for alert {alert.id} - {scraper_err}")
            elif target_dt < current_date:
                # Target date has passed, mark as fulfilled or expired
                logger.info(f"Agent Scheduler: Target date {alert.target_date} has passed for alert {alert.id}. Marking as expired/fulfilled.")
                alert.is_fulfilled = True
                db.commit()

    finally:
        db.close()
    
    logger.info("Agent Scheduler: Check complete.")


def start_scheduler():
    """
    Initializes and starts the APScheduler.
    """
    scheduler = BackgroundScheduler()
    # Run every 6 hours
    scheduler.add_job(
        check_movie_availability,
        trigger=IntervalTrigger(hours=6),
        id="movie_check_job",
        replace_existing=True,
        next_run_time=datetime.now() + timedelta(seconds=5) # Run 5 seconds after startup for immediate testing
    )
    scheduler.start()
    logger.info("Agent Scheduler: Background scheduler started (runs every 6 hours).")
