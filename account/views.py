from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from .forms import UserRegisterForm

@login_required
def profile_view(request, pk=None):
    if pk is None:
        user = request.user
    else:
        User = get_user_model()
        user = get_object_or_404(User, id=pk)
    
    return render(request, 'registration/profile.html', {
        'profile_user': user,
        'questions': user.user_questions.all()[:5],
        'answers': user.user_answers.all()[:5]
    })

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('polls:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'Аккаунт создан для {self.object.username}!')
        return response