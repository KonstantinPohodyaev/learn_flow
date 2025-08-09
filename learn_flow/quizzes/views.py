from django.shortcuts import render, get_object_or_404, redirect

from courses.models import Lesson
from quizzes.models import UserAnswer, Quiz, Question, UserQuizResult
from quizzes.forms import (
    QuizForm, QuizFormCreate, QuestionFormSet, QuestionForm,
    AnswerFormSet
)


def showing_and_passing_quiz(request, lesson_id):
    current_lesson = get_object_or_404(
        Lesson.objects
        .select_related('module__course')
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
        true_answers_count = 0
        for question in questions:
            answer_pk = int(form.cleaned_data[f'question_{question.pk}'])
            answer = question.answers.get(pk=answer_pk)
            UserAnswer.objects.create(
                user=request.user,
                question=question,
                answer=answer
            )
            if question.answers.filter(pk=answer_pk, is_correct=True).exists():
                true_answers_count += 1
        score = round((true_answers_count / questions.count()) * 100, 0)
        previos_user_result = UserQuizResult.objects.filter(
            user=request.user, quiz=quiz
        ).first()
        new_success_status = score >= quiz.passing_score
        if previos_user_result:
            previos_user_result.score = score
            previos_user_result.success_status = new_success_status
            previos_user_result.save()
        else:
            UserQuizResult.objects.create(
                user=request.user,
                quiz=quiz,
                success_status=new_success_status,
                score=score
            )
        return render(
            request,
            'quizzes/quiz_result.html',
            context=dict(
                lesson=current_lesson,
                quiz_status=new_success_status,
                score=score,
                quiz=quiz
            )
        )
    previos_user_quiz_result = request.user.user_quiz_results.filter(
        quiz=quiz
    ).first()
    return render(
        request,
        'quizzes/quiz_detail.html',
        context=dict(
            quiz=quiz,
            lesson=current_lesson,
            form=form,
            previos_user_quiz_result=previos_user_quiz_result
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
        question_formset = QuestionFormSet(request.POST, queryset=Question.objects.none())
        if question_formset.is_valid():
            questions = question_formset.save(commit=False)
            valid = True
            answer_formsets = []
            for index, question in enumerate(questions):
                question.quiz = quiz
                answer_formset = AnswerFormSet(
                    request.POST,
                    instance=question,
                    prefix=f'answers_{index}'
                )
                answer_formsets.append(answer_formset)
                if not answer_formset.is_valid():
                    valid = False
            if valid:
                for index, question in enumerate(questions):
                    question.quiz = quiz
                    question.save()
                    answer_formsets[index].instance = question
                    answer_formsets[index].save()
                return redirect('quizzes:quiz_passing', lesson_id=quiz.lesson.id)
        else:
            answer_formsets = [
                AnswerFormSet(prefix=f'answers_{index}') for index in range(question_formset.total_form_count())
            ]
    else:
        question_formset = QuestionFormSet(queryset=Question.objects.none())
        answer_formsets = [
            AnswerFormSet(prefix=f'answers_{index}') for index in range(question_formset.total_form_count())
        ]

    question_answer_formsets = list(zip(question_formset.forms, answer_formsets))
    return render(
        request,
        'quizzes/quiz_add_questions.html',
        context={
            'quiz': quiz,
            'question_formset': question_formset,
            'question_answer_formsets': question_answer_formsets,
        }
    )

