import asyncio
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from loguru import logger
import dotenv

from src.config.mail_config import brevo

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

configuration = brevo()

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


async def send_email(to_email: str, username: str, movie: str, cinema: str, date: str):
    sender = {"name": "n99", "email": "info@nintynine.tech"}
    to = [{"email": to_email, "name": username}]
    subject = f"🎬 Movie Alert: {movie} is now available!"
    html_content = generate_email_content(username, movie, cinema, date)

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, 
        html_content=html_content, 
        sender=sender, 
        subject=subject
    )

    try:
        api_response = await asyncio.to_thread(api_instance.send_transac_email, send_smtp_email)
        logger.info(f"Email to {to_email} sent successfully! Message ID: {api_response.message_id}")
    except ApiException as e:
        logger.error(f"Exception when calling TransactionalEmailsApi->send_transac_email: {e}")


def generate_email_content(username, movie, cinema, date):
    template_path = "src/services/mail/mail_template/index.html"
    with open(template_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    
    html_content = html_content.replace("{{username}}", username)
    html_content = html_content.replace("{{movie}}", movie)
    html_content = html_content.replace("{{cinema}}", cinema)
    html_content = html_content.replace("{{date}}", date)

    return html_content

if __name__ == "__main__":
    # Test the email content generation
    with open("test_email.html", "w", encoding="utf-8") as file:
        file.write(generate_email_content("John Doe", "Inception", "Cinema City", "2024-07-01"))