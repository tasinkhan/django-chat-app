from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(email, username):
    subject = "Welcome to Django Chat"
    message = f"Hi {username}, thanks for joining!"
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])


@shared_task
def send_bulk_email(subject, message, recipient_list):
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, recipient_list)
