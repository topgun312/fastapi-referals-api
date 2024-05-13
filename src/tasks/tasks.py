import smtplib
from email.message import EmailMessage

from celery import Celery

from src.config import (
    REDIS_HOST,
    REDIS_PORT,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USER,
)


celery = Celery("tasks", broker=f"redis://{REDIS_HOST}:{REDIS_PORT}")


def get_email_template_referal_code(username: str, ref_code: str) -> EmailMessage:
    """
    Функция для генерации html-шаблона при получении реферального кода по email
    """
    email = EmailMessage()
    email["Subject"] = "Получи реферальный код"
    email["From"] = SMTP_USER
    email["To"] = SMTP_USER

    email.set_content(
        "<div>"
        f'<h1 style="color: green;">Здравствуй, {username} 😊, Реферальный код для регистрации:</h1>'
        f'<h2 style="color: black; position: absolute;">{ref_code}</h2>'
        "</div>",
        subtype="html",
    )
    return email


@celery.task
def send_email_report_referal_code(username: str, ref_code: str) -> None:
    """
    Функция для отправки сообщения на электронную почту при получении реферального кода по email
    """
    email = get_email_template_referal_code(username, ref_code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
