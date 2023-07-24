import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from api.utils.logger.messages_logger import INFO_EMAIL_SENT, ERROR_EMAIL_SEND_FAILURE
from api.utils.logger.logger import setup_logger

logger = setup_logger(__name__)

def send_email(to, subject, confirmation_url, template_id):
    message = Mail(
        from_email=os.getenv('EMAIL_USER'),
        to_emails=to,
        subject=subject,
    )
    message.template_id = template_id
    message.dynamic_template_data = {"confirmation_url": confirmation_url}

    try:
        sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        logger.info(INFO_EMAIL_SENT.format(status_code=response.status_code))
    except Exception as e:
        logger.error(ERROR_EMAIL_SEND_FAILURE.format(error=e))
