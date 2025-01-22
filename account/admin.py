from django.contrib import admin
from .models import User
from simple_history.admin import SimpleHistoryAdmin


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin):
    list_display = ["bolded_login", "email", 'web_url']
    search_fields = ['username']
