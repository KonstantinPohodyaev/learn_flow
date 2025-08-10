import random

from django import forms
from quizzes.models import Answer, Question, Quiz

QUESTION_FORMSET_EXTRA = 3
ANSWER_FORMSET_EXTRA = 4


class QuizForm(forms.Form):
    """Форма для прохождения теста урока."""

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            choises = [
                (answer.id, answer.text)
                for answer in question.answers.all()
            ]
            random.shuffle(choises)
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choises,
                widget=forms.RadioSelect,
                label=question.text
            )


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']


class QuizFormCreate(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'passing_score']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = dict(
            text=forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            )
        )


QuestionFormSet = forms.modelformset_factory(
    Question,
    form=QuestionForm,
    extra=QUESTION_FORMSET_EXTRA,
    can_delete=False
)


AnswerFormSet = forms.inlineformset_factory(
    Question,
    Answer,
    form=AnswerForm,
    extra=ANSWER_FORMSET_EXTRA,
    can_delete=False
)