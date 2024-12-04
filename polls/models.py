from django.db import models
from django.contrib import admin
from django.utils.html import format_html

# Create your models here.
class Profile(models.Model):
    nickname = models.CharField(max_length=64, verbose_name='Имя')
    email = models.CharField(max_length=320, verbose_name='Электронная почта')
    login = models.CharField(max_length=256, verbose_name='Логин')
    password = models.CharField(max_length=256, verbose_name='Пароль')

    def __str__(self):
        return self.login
    
    @admin.display(ordering="profile__login")
    def bolded_login(self):
        return format_html('<b>{}</b>', self.login)
    
    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'

class Category(models.Model):
    title = models.CharField(max_length=64, verbose_name='Название')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

class Question(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    question_text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.question_text
    
    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = 'Вопрос'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer_text = models.TextField(verbose_name='Текст')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')
    usefull = models.BooleanField(default=False)
    
    def __str__(self):
        return self.answer_text
    
    class Meta:
        verbose_name_plural = 'Ответы'
        verbose_name = 'Ответ'
    
    