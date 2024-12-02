from django.db import models
from django.contrib import admin
from django.utils.html import format_html

# Create your models here.
class Profile(models.Model):
    nickname = models.CharField(max_length=64)
    email = models.CharField(max_length=320)
    login = models.CharField(max_length=256)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.login
    
    @admin.display(ordering="profile__login")
    def bolded_login(self):
        return format_html('<b>{}</b>', self.login)
    
    class Meta:
        verbose_name_plural = 'Пользователи'

class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Категории'

class Question(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text
    
    class Meta:
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.answer_text
    
    class Meta:
        verbose_name_plural = 'Ответы'
    
    