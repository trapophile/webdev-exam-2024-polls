
from rest_framework import generics
from .models import Question, Answer, Category, Profile
from .serializers import QuestionSerializer, AnswerSerializer, CategorySerializer, ProfileSerializer
from rest_framework.filters import SearchFilter
from .filters import QuestionFilter
from django_filters.rest_framework import DjangoFilterBackend

class QuestionListCreate(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['question_text', 'category__title']
    filterset_class = QuestionFilter

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerListCreate(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user', 'answer_text', 'question']

class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class ProfileListCreate(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'nickname', 'login']

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    


