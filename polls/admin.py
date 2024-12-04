from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
from .models import Profile, Category, Question, Answer


@admin.register(Profile)

class ProfileAdmin(SimpleHistoryAdmin):
    list_display = ["nickname", "email", "bolded_login"]
    readonly_fields = ['login']
    search_fields = ['nickname']

@admin.register(Answer)

class AnswerAdmin(SimpleHistoryAdmin):
    date_hierarchy = "pub_date"
    raw_id_fields = ['user']
    list_display = ['custom_name', 'question__question_text', 'user', 'pub_date']
    def custom_name(self, obj):
        return obj.answer_text

@admin.register(Category)

class CategoryAdmin(SimpleHistoryAdmin):
    list_display = ['__str__']

@admin.register(Question)

class QuestionAdmin(SimpleHistoryAdmin):
    list_filter = ['category']
    date_hierarchy = 'pub_date'
    list_display = ["user", "question_text", "category", "pub_date"]
    list_display_links = ['question_text']

