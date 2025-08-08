from django import forms


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
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choises,
                widget=forms.RadioSelect,
                label=question.text
            )
