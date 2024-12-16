
from django.urls import path, include
from .views import QuestionViewSet, QuestionDetail, AnswerViewSet, CategoryViewSet, CategoryDetail, ProfileViewSet, ProfileDetail, AnswerDetail, question_list, question_detail
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('api/questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('api/categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('api/profiles/<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
    path('api/answers/<int:pk>/', AnswerDetail.as_view(), name='answer-detail'),
    path('api/', include(router.urls)),
    path('', question_list, name='question_list'),
    path('question/<int:question_id>/', question_detail, name='question_detail'),
]
