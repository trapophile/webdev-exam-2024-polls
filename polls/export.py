from import_export.resources import ModelResource
from .models import Question

class QuestionResource(ModelResource):
    class Meta:
        model = Question
        fields = ['user', 'category', 'question_text', 'pub_date']