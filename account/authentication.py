from .models import User

def create_profile(backend, user, *args, **kwargs):
 
 User.objects.get_or_create(id=user.id, defaults={
        'username': user.username,
        'email': user.email
    })