
from django.urls import path
from .views import QuestionListCreate, QuestionDetail, AnswerListCreate, AnswerDetail, CategoryListCreate, CategoryDetail, ProfileListCreate, ProfileDetail

urlpatterns = [
    path('questions/', QuestionListCreate.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('answers/', AnswerListCreate.as_view(), name='answer-list-create'),
    path('answers/<int:pk>/', AnswerDetail.as_view(), name='answer-detail'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('profiles/', ProfileListCreate.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
]