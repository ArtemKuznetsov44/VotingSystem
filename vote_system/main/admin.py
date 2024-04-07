from django.contrib import admin
from .models import *


@admin.register(Anonym)
class AnonymAdmin(admin.ModelAdmin):
    list_display = ('id', 'unique_code', 'voting')


@admin.register(UserParticipant)
class UserParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'voting', 'user')


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url', 'is_open', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    list_editable = ('is_open',)
    search_fields = ('title',)


class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ('id', 'voting', 'question', 'type')
    # As far as I understand, we can use inlines when model in inline has FK to current model.
    inlines = [AnswerInLine]


@admin.register(UserBulletinAnswer)
class UserResultAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'bulletin', 'user')


@admin.register(AnonymBulletinAnswer)
class AnonymResultAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'bulletin', 'anonym')

