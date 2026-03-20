import asyncio
from datetime import datetime, timedelta
import json
import uuid
from zoneinfo import ZoneInfo
from loguru import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.model.core.showg_spider import movies_showing
from src.model.db.data_pg import DataPG
from src.model.db.profile_pg import ProfilePG

from src.services.mail.brevo import send_email

data_pg = DataPG()
profile_pg = ProfilePG()

scheduler = AsyncIOScheduler()
sem = asyncio.Semaphore(3)

async def scheduling_task(**kwargs):
    """Task function to fetch and store currently showing movies."""
    try:
        async with sem:
            result = await movies_showing(
                cinema=kwargs.get('cinema'),
                code=kwargs.get('code'),
                city=kwargs.get('city'),
                target_date=kwargs.get('target_date'),
                movie=kwargs.get('movie'),
            )

        job_id = kwargs.get('ref_job_id')
        if result is True and job_id:
            logger.info(f"Movie '{kwargs['movie']}' is currently showing. Sending notification and removing job {job_id}.")
            user_ids = data_pg.read_userID(job_id)

            for user_id in user_ids:
                user_data = profile_pg.read_user_data(user_id)
                # Send notification email to user_email
                await send_email(
                    to_email=user_data[0][1],
                    username=user_data[0][0],
                    movie=kwargs['movie'],
                    cinema=reverse_lookup(kwargs['cinema']),
                    date=datetime.strptime(kwargs['target_date'], "%Y%m%d").strftime("%d-%m-%Y")
                )

            scheduler.remove_job(job_id)
            data_pg.delete_user_data(job_id)
            logger.info(f"Job {job_id} completed and removed from scheduler.")

    except Exception as e:
        logger.error(f"Error in movies_showing_task: {e}")

def add_new_job(job_id, start_date, **kwargs):
    """
    Creates and adds a job to the running scheduler.
    """
    try:
        # Check if job ID already exists to avoid duplicates
        if scheduler.get_job(job_id):
            logger.info(f"Job {job_id} already exists. Skipping creation.")

        # Add the job to the scheduler
        new_job = scheduler.add_job(
            scheduling_task,
            'interval',
            id=job_id,
            minutes=1,
            start_date=start_date,
            next_run_time=datetime.now(),
            kwargs=kwargs
        )
        logger.info(f"Successfully added Job: {job_id}")
        return new_job
    except Exception as e:
        logger.error(f"Error adding job {job_id}: {e}")

def data_mappg(data):
    try:
        # logger.info(f"Running data_mappg at {datetime.now()}")
        # Read cinema-list.json and map the data to the required format
        with open("src/services/scheduler/cinema-list.json", "r") as f:
            cinema_list = json.load(f)

        movie_mapped_data = []
        job_data = []

        for record in data:
            date_diff = datetime.strptime(record['date'], "%Y-%m-%d").date() - datetime.now(ZoneInfo("Asia/Kolkata")).date()
            if timedelta(days=0) < date_diff <= timedelta(days=3):

                cinema_name = record['cinema']
                if cinema_name in cinema_list['cinema']:
                    cinema_info = cinema_list['cinema'][cinema_name]
                    movie_mapped_record = {
                        "cinema": cinema_info['name'],
                        "code": cinema_info['code'],
                        "city": cinema_info['city'],
                        "date": record['date'],
                        "movie": record['movie'],
                    }

                    job_record = {
                        "job_id": record['job_id'],
                        "date": record['date'],
                    }

                    movie_mapped_data.append(movie_mapped_record)
                    job_data.append(job_record)
                    
                else:
                    logger.info(f"Cinema '{cinema_name}' not found in cinema-list.json. Skipping record.")
        
        return movie_mapped_data, job_data

    except Exception as e:
        logger.error(f"Error in data_mappg: {e}")
        return [], []
    
def reverse_lookup(cinema_var):
    try:
        with open("src/services/scheduler/cinema-list.json", "r") as f:
            cinema_list = json.load(f)

        # Build reverse lookup dict: {name: original_name}
        reverse_lookup_dict = {v['name']: k for k, v in cinema_list['cinema'].items()}

        original_name = reverse_lookup_dict.get(cinema_var)
        return original_name

    except Exception as e:
        logger.error(f"Error in reverse_lookup: {e}")
        return None

async def main():
    try:
        scheduler.start()

        movie_mapped_data, job_data = data_mappg(data_pg.find_job())

        for movie_record, job_record in zip(movie_mapped_data, job_data):
            add_new_job(
                job_id=job_record['job_id'],
                start_date=datetime.strptime(job_record['date'], "%Y-%m-%d"),

                cinema=movie_record['cinema'],
                code=movie_record['code'],
                city=movie_record['city'],
                target_date=movie_record['date'].replace("-", ""),
                movie=movie_record['movie'],
                ref_job_id=job_record['job_id']
            )
    
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    asyncio.run(main())
    # async def main():
    #     scheduler.start()
        
    #     job = add_new_job(
    #         job_id=str(uuid.uuid4()),
    #         date=datetime.now(), # Temporarily set to now for testing
    #         name="inox-janak-place",
    #         code="SCJN",
    #         city="national-capital-region-ncr",
    #         date="20260313"
    #     )
        
    #     try:
    #         while True:
    #             await asyncio.sleep(1)
    #     except (KeyboardInterrupt, SystemExit):
    #         scheduler.shutdown()
    #         print("Scheduler stopped.")

    # asyncio.run(main())
    # t = task_args()
    t = data_mappg([{'date': '2026-03-22', 'movie': 'Kerala Story 2', 'cinema': 'PVR: Vegas Dwarka', 'job_id': 'e54bf73f-8384-443e-b28c-21018574270a'}])
    print(t[0])