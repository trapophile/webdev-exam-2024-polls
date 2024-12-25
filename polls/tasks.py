from celery import shared_task
from django.core.mail import send_mail
from .models import Profile


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
    profiles = Profile.objects.all()
    for profile in profiles:
        send_mail(
            'Новогодняя рассылка',
            f'С новым годом, с новым счастьем, {profile.nickname}!',
            'semkin@kursach.com',
            [profile.email],
            fail_silently=False,
        )
