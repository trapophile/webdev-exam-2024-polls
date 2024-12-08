
from django.urls import path, include
from .views import QuestionViewSet, QuestionDetail, AnswerViewSet, CategoryViewSet, CategoryDetail, ProfileViewSet, ProfileDetail
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
    path('', include(router.urls)),
]