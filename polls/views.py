from django.db.models import Q, Count
from rest_framework import viewsets, generics
from .models import Question, Answer, Category
from .serializers import QuestionSerializer, AnswerSerializer, CategorySerializer, UserSerializer
from rest_framework.filters import SearchFilter
from .filters import QuestionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
import weasyprint
from django.http import HttpResponse
from account.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import QuestionForm, AnswerForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def home(request):
    popular_categories = cache.get('popular_categories')
    if not popular_categories:
        print("Данные извлекаются из базы данных")
        popular_categories = Category.objects.annotate(question_count=Count('question')).order_by('-question_count')[:5]
        cache.set('popular_categories', popular_categories, timeout=60 * 15)
    else:
        print("Данные получены из кэша")

    unanswered_questions = cache.get('unanswered_questions')
    if not unanswered_questions:
        print("Данные извлекаются из базы данных")
        unanswered_questions = Question.objects.filter(question_answers__isnull=True).distinct()[:5]
        cache.set('unanswered_questions', unanswered_questions, timeout=60 * 15)
    else:
        print("Данные получены из кэша")

    active_users = cache.get('active_users')
    if not active_users:
        print("Данные извлекаются из базы данных")
        active_users = User.objects.annotate(answer_count=Count('user_answers')).order_by('-answer_count')[:5]
        cache.set('active_users', active_users, timeout=60 * 15)
    else:
        print("Данные получены из кэша")

    context = {
        'popular_categories': popular_categories,
        
        'unanswered_questions': unanswered_questions,
        
        'active_users': active_users,
    }
    return render(request, 'polls/home.html', context)

def admin_answer_pdf(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    html = render_to_string('admin/answers/answer/pdf.html', {'answer': answer})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=answer_{answer.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('pub_date')
    serializer_class = QuestionSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['question_title', 'category__title']
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
    search_fields = ['user', 'answer_text', 'question__question_title']

    @action(methods=['POST', 'GET'], detail=True)
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username']


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


class CategoryListView(ListView):
    model = Category
    template_name = 'polls/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(
            question_count=Count('question')
        ).order_by('title')


class QuestionListView(ListView):
    model = Question
    template_name = 'polls/question_list.html'
    context_object_name = 'questions'
    ordering = ['-pub_date']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        user_id = self.request.GET.get('user')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category')
        user_id = self.request.GET.get('user')
        
        if category_id:
            context['category'] = Category.objects.get(id=category_id)
        if user_id:
            context['filtered_user'] = User.objects.get(id=user_id)
            
        return context


class AnswerListView(ListView):
    model = Answer
    template_name = 'polls/answer_list.html'
    context_object_name = 'answers'
    paginate_by = 10

    def get_queryset(self):
        return Answer.objects.select_related('user', 'question').annotate(
            like_count=Count('likes')
        ).order_by('-like_count', '-pub_date')


class UserListView(ListView):
    model = User
    template_name = 'polls/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        return User.objects.annotate(
            question_count=Count('user_questions'),
            answer_count=Count('user_answers')
        ).order_by('username')


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'polls/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = self.object.question_answers.select_related('user').annotate(
            like_count=Count('likes')
        ).order_by('-status', '-like_count', '-pub_date')
        return context

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'polls/question_form.html'
    success_url = reverse_lazy('polls:question_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'polls/question_form.html'
    
    def test_func(self):
        question = self.get_object()
        return self.request.user == question.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('account:login')
        raise PermissionDenied("У вас нет прав для редактирования этого вопроса")

    def get_success_url(self):
        return reverse('polls:question_detail', kwargs={'pk': self.object.pk})

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('polls:question_list')
    
    def test_func(self):
        question = self.get_object()
        return self.request.user == question.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('account:login')
        raise PermissionDenied("У вас нет прав для удаления этого вопроса")

    template_name = 'polls/question_confirm_delete.html'


class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'polls/answer_form.html'

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.user

    def get_success_url(self):
        answer = self.get_object()
        return reverse('polls:question_detail', kwargs={'pk': answer.question.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.get_object().question  # добавляем вопрос в контекст
        return context

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    
    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.user

    def get_success_url(self):
        return reverse('polls:question_detail', kwargs={'pk': self.object.question.pk})

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('account:login')
        raise PermissionDenied("У вас нет прав для удаления этого ответа")

@login_required
def mark_answer_useful(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    question = answer.question
    question_id = question.id  # явно получаем ID вопроса
    
    if request.user != question.user:
        messages.error(request, 'Только автор вопроса может отмечать ответы как полезные')
        return redirect('polls:question_detail', pk=question_id)
    
    if answer.status == 'US':
        answer.status = 'NO'
        messages.success(request, 'Отметка о полезном ответе снята')
    else:
        question.question_answers.filter(status='US').update(status='NO')
        answer.status = 'US'
        messages.success(request, 'Ответ отмечен как полезный')
    
    answer.save()
    return redirect('polls:question_detail', pk=question_id)

class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'polls/answer_form.html'

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        form.instance.question = question
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.kwargs['question_id'])
        return context

    def get_success_url(self):
        return reverse('polls:question_detail', kwargs={'pk': self.kwargs['question_id']})
