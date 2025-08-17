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



custom_admin_site.register(Question)
custom_admin_site.register(Answer)
custom_admin_site.register(UserAnswer)
custom_admin_site.register(UserQuizResult)
