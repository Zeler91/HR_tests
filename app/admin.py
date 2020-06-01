from django.contrib import admin
from app.models import Question, Test, UserProfile, Result

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('tests',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass
    # filter_horizontal = ('tests',)
# Register your models here.
