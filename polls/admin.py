from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Category, Question, Answer
from import_export.admin import ExportActionModelAdmin
from .export import AnswerResource, CategoryResource
from django.urls import reverse
from django.utils.safestring import mark_safe


class AnswerInLine(admin.TabularInline):
    model = Answer


def answer_pdf(obj):
    url = reverse('admin_answer_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
answer_pdf.short_description = 'PDF'


@admin.register(Answer)
class AnswerAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    date_hierarchy = "pub_date"
    raw_id_fields = ['user']
    list_display = ['answer_text', 'status', 'question__question_title', 'user', 'pub_date', answer_pdf]
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
    list_display = ["user", "question_title", "category", "pub_date"]
    list_display_links = ['question_title']
    readonly_fields = ['pub_date']


    def get_export_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(category__id__in=['1', '2', '3'])
