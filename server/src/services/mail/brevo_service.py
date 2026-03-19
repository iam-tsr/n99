import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from loguru import logger

class BrevoService:
    def __init__(self):
        self.api_key = os.getenv("BREVO_API_KEY")
        self.sender_email = os.getenv("SENDER_EMAIL", "notifications@n99.com")
        self.sender_name = os.getenv("SENDER_NAME", "n99 Movie Alerts")
        
        if not self.api_key:
            logger.warning("BREVO_API_KEY not found in environment variables.")
            
        # Configure API key authorization
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = self.api_key

    async def send_movie_alert(self, to_email: str, to_name: str, movie_name: str, cinema: str, date: str):
        """Sends an email alert when a movie is found."""
        if not self.api_key:
            logger.error("Cannot send email: BREVO_API_KEY is missing.")
            return False

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        
        subject = f"🎬 Movie Alert: {movie_name} is now showing!"
        html_content = f"""
        <html>
            <body>
                <h1>Good news, {to_name}!</h1>
                <p>The movie <strong>{movie_name}</strong> you were tracking is now showing at <strong>{cinema}</strong> on <strong>{date}</strong>.</p>
                <p>Go grab your tickets now!</p>
                <br>
                <p>Best regards,<br>n99 Team</p>
            </body>
        </html>
        """
        
        sender = {{"name": self.sender_name, "email": self.sender_email}}
        to = [{{"email": to_email, "name": to_name}}]
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject
        )

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            logger.info(f"Email sent successfully to {to_email}. Response: {api_response}")
            return True
        except ApiException as e:
            logger.error(f"Exception when calling TransactionalEmailsApi->send_transac_email: {e}")
            return False
