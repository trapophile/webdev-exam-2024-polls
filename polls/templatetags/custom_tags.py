from django import template
from ..models import Question


register = template.Library()

@register.simple_tag
def simple_tag():
    return "Это простой шаблонный тег!"

@register.simple_tag(takes_context=True)
def context_tag(context, variable_name):
    value = context.get(variable_name, None)
    if value is not None:
        return f"Значение переменной {variable_name}: {value}"
    else:
        return f"Переменная {variable_name} отсутствует в контексте."
    
from ..models import Question

@register.inclusion_tag('question/question_list_tag.html')
def queryset_tag():
    questions = Question.objects.all()[:5]
    return {'questions': questions}