from django.contrib import admin

from quizzes.models import Answer, Question, Quiz, UserAnswer, UserQuizResult
from core_admin.admin_site import custom_admin_site


QUIZ_ADMIN_QUESTION_COUNT_DESCRIPTION = 'Количество вопросов'


@admin.register(Quiz, site=custom_admin_site)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'lesson__title',
        'passing_score',
        'question_count'
    ]
    search_fields = [
        'title',
        'lesson__title'
    ]
    list_filter = [
        'title',
        'lesson__title'
    ]
    list_display_links = [
        'title'
    ]

    @admin.display(
        description=QUIZ_ADMIN_QUESTION_COUNT_DESCRIPTION
    )
    def question_count(self, quiz):
        return quiz.questions.count()


@admin.register(Question, site=custom_admin_site)
class QuestionSite(admin.ModelAdmin):
    list_display = [
        'quiz__title',
        'text'
    ]
    search_fields = [
        'text'
    ]
    list_filter = [
        'text'
    ]
    list_display_links = [
        'text'
    ]


@admin.reggister(Answer, site=custom_admin_site)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'question__quiz__title',
        'text',
        'is_correct'
    ]
    search_fields = [
        'text'
    ]
    list_filter = [
        'text',
        'is_correct'
    ]
    list_display_links = [
        'text'
    ]


custom_admin_site.register(UserAnswer)
custom_admin_site.register(UserQuizResult)
