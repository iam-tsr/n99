from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
from src.config.db_config import get_db_connection
from src.model.core.avail_spider import avail_movies

scheduler = BackgroundScheduler()

def avail_movies_task():
    """Task function to fetch and store available movies."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            if cur.execute("SELECT id FROM movie_data WHERE id = 'AVAIL'"):
                logger.info("Movie availability record already exists. Updating it.")
                movies = avail_movies()

                cur.execute("""
                UPDATE movie_data
                SET movie_titles = %s, updated_at = %s
                WHERE id = 'AVAIL';
                """, (movies, datetime.now(tz=ZoneInfo('Asia/Kolkata'))))

        conn.commit()
        logger.info("Updated available movies in available_movies.")

    except Exception as e:
        logger.error("Connection failed.")
        logger.error(e)

    finally:
        conn.close()


def start_scheduler():
    """Starts the scheduler and adds the movie availability task."""
    scheduler.add_job(avail_movies_task, 'interval', days=2, next_run_time=datetime.now())
    scheduler.start()
    logger.info("Scheduler started. Movie availability will be checked every hour.")

if __name__ == "__main__":
    start_scheduler()
    
    # Keep the main thread alive to let the scheduler run
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")