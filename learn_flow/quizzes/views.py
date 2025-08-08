from django.shortcuts import render, get_object_or_404

from courses.models import Lesson
from quizzes.forms import QuizForm


def showing_and_passing_quiz(request, lesson_id):
    current_lesson = get_object_or_404(
        Lesson.objects.select_related('module__course'), pk=lesson_id
    )
    try:
        quiz = current_lesson.quiz
    except Lesson.quiz.RelatedObjectDoesNotExist:
        return render(
            request,
            'quizzes/quiz_not_exist.html',
            context=dict(
                lesson=current_lesson
            )
        )
    questions = current_lesson.objects.prefetch_related('answers').all()
    form = QuizForm(request.POST or None, questions=questions)
    if request.methos == 'POST' and form.is_valid():
        score = 0
        for question in questions:
            answer_pk = int(form.cleaned_data[f'question_{question.pk}'])
            if question.answers.filter(pk=answer_pk, is_correct=True).exists():
                score += 1
        quiz_status = score >= quiz.passing_score
        return render(
            request,
            'quizzes/quiz_result.html',
            context=dict(
                lesson=current_lesson,
                quiz_status=quiz_status,
                score=score
            )
        )
    return render(
        request,
        'quizzes/quiz_detail.html',
        context=dict(
            quiz=quiz,
            lesson=current_lesson,
            form=form
        )
    )
