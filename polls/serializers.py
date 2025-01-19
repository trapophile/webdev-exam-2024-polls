from rest_framework import serializers
import re
from .models import Question, Category, Answer
from account.models import User


class AnswerSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer_text', 'user', 'pub_date', 'status', 'likes_count']

    def validate_answer_text(self, text):
        if not text:
            raise serializers.ValidationError('Ответ не может быть пустым.')
        if len(text) < 10:
            raise serializers.ValidationError('Ответ должен содержать не менее 10 символов.')
        return text


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_login(self, value):
        if not value:
            raise serializers.ValidationError('Логин не может быть пустым.')
        if not re.match(r"^[a-zA-Z\s]+$", value):
            raise serializers.ValidationError(
                "Логин может быть написан только на латинице."
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Question
        fields = '__all__'
