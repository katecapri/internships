from uuid import uuid4
import json
import logging

from src.message_broker.producer import send_into_email_queue

logger = logging.getLogger('app')


def send_email(email_content: str, email_to: str):
    try:
        new_email_event_id = uuid4()
        email_info = {
            "id": str(new_email_event_id),
            "emailContent": email_content,
            "emailTo": email_to
        }
        send_into_email_queue(json.dumps(email_info))
        logger.info(f'Email to {email_to} was sent to the queue.')
        return True
    except Exception as e:
        logger.error(e, exc_info=True)
        return False
