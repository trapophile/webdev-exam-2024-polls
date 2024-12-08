from django.db.models import Q, Count
from rest_framework import viewsets, generics
from .models import Question, Answer, Category, Profile
from .serializers import QuestionSerializer, AnswerSerializer, CategorySerializer, ProfileSerializer
from rest_framework.filters import SearchFilter
from .filters import QuestionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('pub_date')
    serializer_class = QuestionSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['question_text', 'category__title']
    filterset_class = QuestionFilter

    @action(methods=['GET'], detail=False)
    def filter_music_questions(self, request):
        query = Q(user__in = ['1', '2', '3']) & ~Q(category__lte = 5) | Q(question_text__startswith = 'Почему')
        usefull_answers = self.queryset.filter(query)
        serializer = self.get_serializer(usefull_answers, many=True)
        return Response(serializer.data)

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user', 'answer_text', 'question']

    @action(methods=['POST', 'GET'], detail=True)
    def mark_as_usefull(self, request, pk=None):
        try:
            answer = self.get_object()
        except Answer.DoesNotExist:
            return Response({"error": "Ответ не найден"}, status=404) 
        answer.usefull = True
        answer.save()

        return Response({"message": f"Ответ '{answer.answer_text}' помечен полезным."})
    
    @action(methods=['GET'], detail=False)
    def get_usefull_answers(self, request):
        usefull_answers = self.queryset.filter(usefull=True)
        serializer = self.get_serializer(usefull_answers, many=True)
        return Response(serializer.data)
    
    @action(methods=['GET'], detail=False)
    def filter_usefull_answers(self, request):
        query = Q(user = '2') & ~Q(usefull = False) | Q(answer_text__startswith = 'сайт')
        usefull_answers = self.queryset.filter(query)
        serializer = self.get_serializer(usefull_answers, many=True)
        return Response(serializer.data)
    

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'nickname', 'login']

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    


