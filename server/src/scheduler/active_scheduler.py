import asyncio
from datetime import datetime
import uuid

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.model.core.showg_spider import movies_showing

scheduler = AsyncIOScheduler()

async def movies_showing_task(**spider_kwargs):
    """Task function to fetch and display currently showing movies."""
    movies = await movies_showing(**spider_kwargs)
    return movies

def add_new_job(job_id, trigger_type, duration, start_date, **spider_kwargs):
    """
    Creates and adds a job to the running scheduler.
    
    :param job_id: Unique string to identify this job
    :param trigger_type: 'interval', 'cron', or 'date'
    :param duration: Duration for the interval trigger
    :param start_date: Start date for the date trigger
    :param spider_kwargs: Keyword arguments to pass to the movies_showing_task
    """
    try:
        # Check if job ID already exists to avoid duplicates
        if scheduler.get_job(job_id):
            print(f"Job {job_id} already exists. Updating instead.")

        # Add the job to the scheduler
        new_job = scheduler.add_job(
            movies_showing_task,
            trigger_type,
            id=job_id,
            seconds=duration,
            start_date=start_date,
            kwargs=spider_kwargs
        )
        print(f"Successfully added Job: {job_id}")
        return new_job
    except Exception as e:
        print(f"Error adding job {job_id}: {e}")



if __name__ == "__main__":

    async def main():
        scheduler.start()
        
        job = add_new_job(
            job_id=str(uuid.uuid4()),
            trigger_type='interval',
            duration=5,
            start_date=datetime.now(), # Temporarily set to now for testing
            name="inox-janak-place",
            code="SCJN",
            city="national-capital-region-ncr",
            date="20260313"
        )
        
        try:
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            print("Scheduler stopped.")

    asyncio.run(main())