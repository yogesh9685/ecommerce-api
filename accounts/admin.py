from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin

@admin.register(CustomUser)
class CustomUser(UserAdmin):
    pass

