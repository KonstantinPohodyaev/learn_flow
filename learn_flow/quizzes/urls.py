from django.urls import path

from quizzes.views import showing_and_passing_quiz


app_name = 'quizzes'


urlpatterns = [
    path(
        'quiz/lesson/<int:lesson_id>/',
        showing_and_passing_quiz,
        name='quiz_passing'
    )
]
