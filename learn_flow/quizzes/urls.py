from django.urls import path
from quizzes.views import add_questions, quiz_create, showing_and_passing_quiz

app_name = 'quizzes'


urlpatterns = [
    path(
        'lesson/<int:lesson_id>/',
        showing_and_passing_quiz,
        name='quiz_passing'
    ),
    path(
        'create/lesson/<int:lesson_id>/',
        quiz_create,
        name='quiz_create'
    ),
    path(
        'add-questions/quiz/<int:quiz_id>/',
        add_questions,
        name='add_questions'
    )
]
