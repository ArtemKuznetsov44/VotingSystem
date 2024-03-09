from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Anonym)
class AnonymAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'voting']


@admin.register(MembersList)
class MembersListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'voting']
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
    list_display = ['id', 'type', 'bulletin', 'answers']


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
