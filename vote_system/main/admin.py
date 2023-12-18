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


@admin.register(Anonym)
class AnonymAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'voting']


@admin.register(MembersList)
class MembersListAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'voting']
    list_display_links = ['id']


@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'voting', 'created_at', 'updated_at']
    search_fields = ['id', 'title', 'voting']


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'special_info', 'is_open', 'created_at', 'updated_at', 'options']
    search_fields = ['id', 'title']


@admin.register(VotingOption)
class VotingOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'options']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'bulletin']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'question']


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']


@admin.register(UserResult)
class UserResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'voting', 'user', 'answers']
    search_fields = ['voting', 'user']


@admin.register(AnonymResult)
class AnonymResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'voting', 'anonym', 'answers']
