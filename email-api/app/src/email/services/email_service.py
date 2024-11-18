import os
import smtplib
import logging


from src.email.services.email_repository import EmailRepository

logger = logging.getLogger('app')


def send_email(email_event_id, email_to, content):
    server = smtplib.SMTP(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT"))
    server.starttls()
    server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
    server.set_debuglevel(1)
    server.sendmail(os.getenv("SMTP_USERNAME"), email_to,
                    u''.join(content).encode('utf-8').strip())
    server.quit()
    logger.info(f'Mail is sent to email {email_to}')

    db = EmailRepository()
    result = db.save_email_event(email_event_id, email_to)
    return email_event_id if result else None
