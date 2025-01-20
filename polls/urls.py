from django.urls import path, include
from .views import (QuestionViewSet, QuestionDetail, AnswerViewSet, 
    CategoryViewSet, CategoryDetail, UserViewSet, UserDetail, AnswerDetail,
    admin_answer_pdf, home, CategoryListView, 
    QuestionListView, AnswerListView, UserListView, 
    QuestionDetailView, QuestionCreateView, QuestionUpdateView,
    QuestionDeleteView, answer_create, answer_update, answer_delete,
    mark_answer_useful) 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)

app_name = 'polls'

urlpatterns = [
    path('api/questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('api/categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('api/answers/<int:pk>/', AnswerDetail.as_view(), name='answer-detail'),
    path('api/', include(router.urls)),
    path('admin/answer/<int:answer_id>/pdf/', admin_answer_pdf, name='admin_answer_pdf'),
    path('', home, name='home'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('answers/', AnswerListView.as_view(), name='answer_list'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question/new/', QuestionCreateView.as_view(), name='question_create'),
    path('question/<int:pk>/edit/', QuestionUpdateView.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    path('question/<int:question_id>/answer/', answer_create, name='answer_create'),
    path('answer/<int:pk>/edit/', answer_update, name='answer_update'),
    path('answer/<int:pk>/delete/', answer_delete, name='answer_delete'),
    path('answer/<int:pk>/mark-useful/', mark_answer_useful, name='mark_answer_useful'),
]
