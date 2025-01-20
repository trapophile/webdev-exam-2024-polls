import django_filters
from .models import Question


class QuestionFilter(django_filters.FilterSet):
    question_text_contains = django_filters.CharFilter(field_name='question_title', lookup_expr='icontains', label='Текст вопроса содержит')
    category_title_contains = django_filters.CharFilter(field_name='category__title', label='Название категории', lookup_expr='icontains')
    pub_date_is = django_filters.DateFilter(field_name='pub_date', lookup_expr='date', label='Дата публикации')
    pub_after = django_filters.DateFilter(field_name='pub_date', lookup_expr='gt', label='Опубликован позже')
    pub_before = django_filters.DateFilter(field_name='pub_date', lookup_expr='lt', label='Опубликован раньше')

    class Meta:
        model = Question
        fields = ['question_text_contains', 'category_title_contains', 'pub_date_is', 'pub_after', 'pub_before']
