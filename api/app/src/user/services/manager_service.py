import os
from uuid import UUID

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.services.email_service import send_email


def build_reset_password_email(subject, email_to, confirm_code) -> str:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = os.getenv("SMTP_USERNAME")
    msg['To'] = email_to
    password_reset_link = f"{os.getenv('FRONTEND_URL')}/password-reset?code={confirm_code}"
    html = f"""\
    <html>
      <head></head>
      <body>
        <p>Здравствуйте!<br>
          Для восстановления пароля воспользуйтесь ссылкой<br>
          <a href="{password_reset_link}">{password_reset_link}</a>
        </p>
      </body>
    </html>
    """
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    return msg.as_string()


def send_reset_password_email(email: str, confirm_code: UUID):
    subject = "Восстановление пароля"
    is_sent = send_email(
        build_reset_password_email(subject, email, confirm_code), email
    )
    return is_sent


def build_confirm_email_email(subject, email_to, confirm_code) -> str:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = os.getenv("SMTP_USERNAME")
    msg['To'] = email_to
    confirm_email_link = f"{os.getenv('FRONTEND_URL')}/confirm-email?code={confirm_code}"
    html = f"""\
    <html>
      <head></head>
      <body>
        <p>Здравствуйте!<br>
          Для подтверждения электронной почты воспользуйтесь ссылкой<br>
          <a href="{confirm_email_link}">{confirm_email_link}</a>
        </p>
      </body>
    </html>
    """
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    return msg.as_string()


def send_confirm_email_email(email: str, confirm_code: UUID):
    subject = "Подтверждение электронной почты"
    is_sent = send_email(
        build_confirm_email_email(subject, email, confirm_code), email
    )
    return is_sent
