from django.shortcuts import render, get_object_or_404, redirect

from courses.models import Lesson
from quizzes.models import UserAnswer, Quiz, Question
from quizzes.forms import QuizForm, QuizFormCreate, QuestionFormSet


def showing_and_passing_quiz(request, lesson_id):
    current_lesson = get_object_or_404(
        Lesson.objects
        .select_related('module__course', 'quiz')
        .prefetch_related('quiz__questions__answers'), pk=lesson_id
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
    questions = quiz.questions.all()
    form = QuizForm(request.POST or None, questions=questions)
    if request.method == 'POST' and form.is_valid():
        score = 0
        for question in questions:
            answer_pk = int(form.cleaned_data[f'question_{question.pk}'])
            answer = question.answers.get(pk=answer_pk)
            UserAnswer.objects.create(
                user=request.user,
                question=question,
                answer=answer
            )
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


def quiz_create(request, lesson_id):
    lesson = get_object_or_404(
        Lesson.objects.select_related('module__course').all(),
        pk=lesson_id
    )
    if hasattr(lesson, 'quiz'):
        return redirect('quizzes:quiz_passing', lesson_id=lesson.id)
    if request.method == 'POST':
        form = QuizFormCreate(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.lesson = lesson
            quiz.save()
            return redirect('quizzes:quiz_passing', lesson_id=lesson.pk)
    else:
        form = QuizFormCreate()
    return render(
        request,
        'quizzes/quiz_create.html',
        context=dict(
            form=form, lesson=lesson
        )
    )


def add_questions(request, quiz_id):
    quiz = get_object_or_404(
        Quiz.objects.select_related('lesson').all(),
        pk=quiz_id
    )
    if request.method == 'POST':
        formset = QuestionFormSet(
            request.POST, queryset=Question.objects.none()
        )
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    question = form.save(commit=False)
                    question.quiz = quiz
                    question.save()
            return redirect('quizzes:quiz_passing', lesson_id=quiz.lesson.pk)
    else:
        formset = QuestionFormSet(queryset=Question.objects.none())
    return render(
        request,
        'quizzes/quiz_add_questions.html',
        context=dict(
            quiz=quiz,
            formset=formset
        )
    )
