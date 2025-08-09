from django.contrib import admin

from .models import Quiz, Question, Answer, UserAnswer, UserQuizResult


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserAnswer)
admin.site.register(UserQuizResult)
