from celery import shared_task
from django.core.mail import send_mail
from account.models import User


@shared_task
def send_email_every_minute():
    send_mail(
        'Письмо раз в минуту',
        'Привет, получатель!',
        'semkin379@gmail.com',
        ['recipient@example.com'],
        fail_silently=False,
    )


@shared_task
def send_email_new_year():
    users = User.objects.all()
    for user in users:
        send_mail(
            'Новогодняя рассылка',
            f'С новым годом, с новым счастьем, {user.nickname}!',
            'semkin@kursach.com',
            [user.email],
            fail_silently=False,
        )
