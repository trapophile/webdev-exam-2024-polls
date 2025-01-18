from django.db.models import Q, Count
from rest_framework import viewsets, generics
from .models import Question, Answer, Category, Profile
from .serializers import QuestionSerializer, AnswerSerializer, CategorySerializer, ProfileSerializer
from rest_framework.filters import SearchFilter
from .filters import QuestionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def question_list(request):
    question_list = cache.get('questions_list')

    if not question_list:
        print("Данные извлекаются из базы данных")
        question_list = Question.objects.select_related('user', 'category').all()
        cache.set('questions_list', question_list, timeout=60 * 15)
    else:
        print("Данные получены из кэша")

    paginator = Paginator(question_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        questions = paginator.page(page_number)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'question/question_list.html', {'questions': questions})


def question_detail(request, question_id):
    question_cache_key = f'question_{question_id}'
    question = cache.get(question_cache_key)

    if not question:
        print("Данные извлекаются из базы данных")
        question = get_object_or_404(Question.objects.prefetch_related('question_answers'), id=question_id)
        cache.set(question_cache_key, question, timeout=60 * 15)
    else:
        print("Данные получены из кэша")

    answers = question.question_answers.annotate(likes_count=Count('likes'))

    return render(request, 'question/question_detail.html', {'question': question, 'answers': answers})


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('pub_date')
    serializer_class = QuestionSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['question_text', 'category__title']
    filterset_class = QuestionFilter

    @action(methods=['GET'], detail=False)
    def filter_music_questions(self, request):
        query = Q(user__in=['1', '2', '3']) & ~Q(category__lte=5) | Q(question_text__startswith='Почему')
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
    search_fields = ['user', 'answer_text', 'question__question_text']

    @action(methods=['POST' 'GET'], detail=True)
    def mark_as_usefull(self, request, pk=None):
        answer = get_object_or_404(Answer.objects.filter(id=pk))
        answer.status = 'US'
        answer.save()

        return Response({"message": f"Ответ '{answer.answer_text}' помечен полезным."}, status=200)

    @action(methods=['GET'], detail=False)
    def get_usefull_answers(self, request):
        usefull_answers = Answer.objects.exclude(status='NO')
        serializer = self.get_serializer(usefull_answers, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def filter_usefull_answers(self, request):
        query = Q(user='2') & ~Q(status='NO') | Q(answer_text__startswith='сайт')
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


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer