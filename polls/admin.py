from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Profile, Category, Question, Answer
from import_export.admin import ExportActionModelAdmin
from .export import AnswerResource, CategoryResource


@admin.register(Profile)
class ProfileAdmin(SimpleHistoryAdmin):
    list_display = ["nickname", "email", "bolded_login", "login"]
    search_fields = ['nickname']


class AnswerInLine(admin.TabularInline):
    model = Answer


@admin.register(Answer)
class AnswerAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    date_hierarchy = "pub_date"
    raw_id_fields = ['user']
    list_display = ['answer_text', 'status', 'question__question_text', 'user', 'pub_date']
    readonly_fields = ['pub_date']
    filter_horizontal = ['likes']

    resource_class = AnswerResource


@admin.register(Category)
class CategoryAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    list_display = ['__str__']
    resource_class = CategoryResource


@admin.register(Question)
class QuestionAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    list_filter = ['category']
    date_hierarchy = 'pub_date'
    inlines = [AnswerInLine]
    list_display = ["user", "question_text", "category", "pub_date"]
    list_display_links = ['question_text']
    readonly_fields = ['pub_date']


    def get_export_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(category__id__in=['1', '2', '3'])
