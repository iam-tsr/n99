from services.agent_scheduler import check_movie_availability
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("Manually triggering full agent check...")
    check_movie_availability()
    print("Agent check completed.")
