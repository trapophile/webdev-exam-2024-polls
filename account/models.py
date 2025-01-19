from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(verbose_name='Фото', blank=True, upload_to='avatars/')
    web_url = models.URLField(verbose_name="Ссылка", blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.username

    @admin.display(ordering="profile__username")
    def bolded_login(self):
        return format_html('<b>{}</b>', self.username)

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
