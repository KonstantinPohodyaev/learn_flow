from django.contrib import admin

from quizzes.models import Answer, Question, Quiz, UserAnswer, UserQuizResult
from core_admin.admin_site import custom_admin_site

custom_admin_site.register(Quiz)
custom_admin_site.register(Question)
custom_admin_site.register(Answer)
custom_admin_site.register(UserAnswer)
custom_admin_site.register(UserQuizResult)
