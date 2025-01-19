
from django.urls import path, include
from .views import QuestionViewSet, QuestionDetail, AnswerViewSet, CategoryViewSet, CategoryDetail, UserViewSet, UserDetail, AnswerDetail, question_list, question_detail, admin_answer_pdf
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('api/questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('api/categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('api/answers/<int:pk>/', AnswerDetail.as_view(), name='answer-detail'),
    path('api/', include(router.urls)),
    path('', question_list, name='question_list'),
    path('question/<int:question_id>/', question_detail, name='question_detail'),
    path('admin/answer/<int:answer_id>/pdf/', admin_answer_pdf, name='admin_answer_pdf'),
]
