from celery import shared_task
from django.core.mail import send_mail
@shared_task
def sending_mail(email,code):
    link = "http://127.0.0.1:8000/change/{0}".format(code)
    send_mail("Reset password",
                "your password reset link : {0}".format(link),
                "Django E-Commerce",
                [email]
        )