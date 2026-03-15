import os
import smtplib
from email.message import EmailMessage
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", SMTP_USERNAME)

def send_notification_email(to_email: str, movie_name: str, cinema_place: str, target_date: str, booking_link: str = None):
    """
    Sends an email notification to the user when their requested movie becomes available.
    """
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        logger.warning(f"SMTP Credentials not configured. Would have sent email to {to_email} for {movie_name}.")
        return False
        
    msg = EmailMessage()
    msg['Subject'] = f"🎬 Tickets Available for {movie_name}!"
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    
    body = f"""Hello!

Good news! The AI Agent Scheduler has detected that tickets are now available for your monitored movie:

Movie: {movie_name}
Location: {cinema_place}
Date: {target_date}

Hurry up and book your tickets!
"""
    if booking_link:
        body += f"\nBooking Link: {booking_link}"
        
    msg.set_content(body)
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        logger.info(f"Successfully sent notification email to {to_email} for {movie_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False
