from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Category, Answer, Question
from django import forms
from account.models import User


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'image', 'document']
        widgets = {
            'answer_text': forms.Textarea(attrs={'rows': 10, 'cols': 80, 'placeholder': ('Введите ответ')}),
        }

    def clean_answer_text(self):
        text = self.cleaned_data['answer_text']
        if not text.strip():
            raise ValidationError(('Ответ не может быть пустым.'))
        return text

    def save(self, commit=True):
        instance = super(AnswerForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_title', 'question_body', 'category', 'image', 'document']

    def clean_question_title(self):
        title = self.cleaned_data['question_title']
        if not title.strip():
            raise ValidationError(('Заголовок вопроса не может быть пустым.'))
        return title

    def save(self, commit=True):
        instance = super(QuestionForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'web_url', 'image')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': ('Введите имя')}),
            'email': forms.EmailInput(attrs={'placeholder': ('Введите электронную почту')}),
            'web_url': forms.URLInput(attrs={'placeholder': ('Введите ссылку')}),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError(('Этот адрес электронной почты уже используется.'))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.web_url = self.cleaned_data['web_url']
        user.image = self.cleaned_data['image']
        if commit:
            user.save()
        return user


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': ('Введите название категории')}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title.strip():
            raise ValidationError(('Название категории не может быть пустым.'))
        return title