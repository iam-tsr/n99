from services.email_service import send_notification_email
import logging

logging.basicConfig(level=logging.INFO)

def test_brevo():
    print("Testing Brevo Email...")
    success = send_notification_email(
        to_email="ansh.chauhan@delhitechnicalcampus.ac.in",
        movie_name="Test Movie",
        cinema_place="Test Cinema",
        target_date="2026-03-15"
    )
    if success:
        print("Test Email Sent Successfully!")
    else:
        print("Test Email Failed! Check the logs above.")

if __name__ == "__main__":
    test_brevo()
