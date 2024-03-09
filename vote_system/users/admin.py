from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'slug',
                    'first_name', 'last_name',
                    'father_name', 'email',
                    'is_staff', 'date_joined']
    list_display_links = ['slug']
    list_editable = ['is_staff']
    list_filter = ['id', 'date_joined']
    search_fields = ['first_name', 'second_name', 'father_name']
    prepopulated_fields = {'slug': ['username']}
