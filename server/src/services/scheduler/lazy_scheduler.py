import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from src.config.db_config import get_db_connection
from src.model.core.avail_spider_pw import avail_movies

scheduler = AsyncIOScheduler()

def _avail_movies_task_sync():
    """Task function to fetch and store available movies."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            if cur.execute("SELECT id FROM movie_data WHERE id = 'AVAIL'"):
                # logger.info("Movie availability record already exists. Updating it.")
                movies = avail_movies()
                if movies not in (None, []):
                    cur.execute("""
                    UPDATE movie_data
                    SET movie_titles = %s, updated_at = %s
                    WHERE id = 'AVAIL';
                    """, (movies, datetime.now(tz=ZoneInfo('Asia/Kolkata'))))

                    conn.commit()
                    logger.info("Updated listed movies")
                    return
                
                logger.info("Couldn't fetch available movies. Skipping update.")

    except Exception as e:
        logger.error("Connection failed.")
        logger.error(e)

    finally:
        conn.close()


async def avail_movies_task():
    # DB and scraping operations are blocking; run them in a worker thread.
    await asyncio.to_thread(_avail_movies_task_sync)


async def start_scheduler():
    """Starts the scheduler and adds the movie availability task."""
    if scheduler.running:
        logger.info("Lazy scheduler is already running.")
        return
    
    scheduler.add_job(
        avail_movies_task, 
        'interval', 
        days=2, 
        next_run_time=datetime.now()
    )
    scheduler.start()
    # logger.info("Scheduler started. Movie availability will be checked every 2 days.")

async def main():
    await start_scheduler()

    # Keep the process alive to let the scheduler run.
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    asyncio.run(main())