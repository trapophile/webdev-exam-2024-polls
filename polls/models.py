from django.db import models
from simple_history.models import HistoricalRecords
from django.utils import timezone
from django.urls import reverse
from account.models import User


class Category(models.Model):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название')
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user_questions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    question_body = models.TextField(verbose_name='Текст', blank=True)
    question_title = models.TextField(verbose_name='Заголовок')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    document = models.FileField(blank=True, upload_to='documents/', verbose_name='Документ')
    image = models.ImageField(verbose_name='Фото', blank=True, upload_to='images/')
    history = HistoricalRecords()

    def __str__(self):
        return self.question_title
    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = 'Вопрос'
        ordering = ['-pub_date']

    def get_absolute_url(self):
        return reverse('question_detail', args=[self.id])


class UsefullManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Answer.Status.USEFULL)

class Answer(models.Model):

    class Status(models.TextChoices):
        USEFULL = 'US', 'Полезный'
        NOT_STATED = 'NO', 'Не указан'

    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='question_answers')
    answer_text = models.TextField(verbose_name='Текст')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user_answers')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    status = models.CharField(max_length=2, default=Status.NOT_STATED, choices=Status.choices, verbose_name='Статус')
    likes = models.ManyToManyField(User, verbose_name='Лайки', related_name='likes_answers', blank=True)
    document = models.FileField(blank=True, upload_to='documents/', verbose_name='Документ')
    image = models.ImageField(verbose_name='Фото', blank=True, upload_to='images/')
    history = HistoricalRecords()

    objects = models.Manager()
    usefull = UsefullManager()

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name_plural = 'Ответы'
        verbose_name = 'Ответ'
        ordering = ['-pub_date']
