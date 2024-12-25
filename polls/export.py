from import_export.resources import ModelResource
from .models import Answer, Category


class AnswerResource(ModelResource):
    class Meta:
        model = Answer
        fields = ['user', 'answer_text', 'id', 'pub_date', 'usefull']

    def dehydrate_usefull(self, obj):
        if obj.usefull:
            return "Полезный ответ"
        else:
            return "Ответ не полезен"

    def dehydrate_pub_date(self, obj):
        return obj.pub_date.strftime('%Y-%m-%d')

    def dehydrate_user(self, obj):
        return str(obj.user)


class CategoryResource(ModelResource):
    class Meta:
        model = Category
        fields = ['title']

    def get_category(self, obj):
        return f"Категория: {obj.title}"

    def dehydrate_title(self, obj):
        return self.get_category(obj)
