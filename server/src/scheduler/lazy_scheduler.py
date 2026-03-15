from apscheduler.schedulers.background import BackgroundScheduler

from src.model.core.avail_spider import avail_movies

scheduler = BackgroundScheduler()

def avail_movies_task():
    """Task function to fetch and display available movies."""
    movies = avail_movies()

def start_scheduler():
    """Starts the scheduler and adds the movie availability task."""
    scheduler.add_job(avail_movies_task, 'interval', seconds=10)
    scheduler.start()
    print("Scheduler started. Movie availability will be checked every hour.")

if __name__ == "__main__":
    start_scheduler()
    
    # Keep the main thread alive to let the scheduler run
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")