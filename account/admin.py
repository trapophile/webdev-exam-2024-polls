from django.contrib import admin
from .models import User
from simple_history.admin import SimpleHistoryAdmin


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin):
    list_display = ["username", "email", "bolded_login", 'web_url']
    search_fields = ['username']
