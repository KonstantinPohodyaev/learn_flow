from django.db import models

QUIZ_TITLE_VERBOSE_NAME = 'Название'
QUIZ_TITLE_MAX_LENGTH = 127
QUIZ_TITLE_HELP_TEXT = 'Введите название теста'
QUIZ_LESSON_VERBOSE_NAME = 'Урок'
QUIZ_PASSING_SCORE_VERBOSE_NAME = 'Проходной балл'
QUIZ_PASSING_SCORE_DEFAULT = 75
QUIZ_PASSING_SCORE_HELP_TEXT = 'Укажите проходной балл'
QUIZ_VERBOSE_NAME = 'Тест'
QUIZ_VERBOSE_NAME_PLURAL = 'Тесты'

QUESTION_QUIZ_VERBOSE_NAME = 'Тест'
QUESTION_TEXT_VERBOSE_NAME = 'Текст вопроса'
QUESTION_TEXT_HELP_TEXT = 'Введите текст вопроса'
QUESTION_VERBOSE_NAME = 'Вопрос'
QUESTION_VERBOSE_NAME_PLURAL = 'Вопросы'

ANSWER_QUESTION_VERBOSE_NAME = 'Вопрос'
ANSWER_TEXT_VERBOSE_NAME = 'Текст варианта ответа'
ANSWER_TEXT_MAX_LENGTH = 255
ANSWER_TEXT_HELP_TEXT = 'Введите текст варипанта ответа'
ANSWER_IS_CORRECT_VERBOSE_NAME = 'Статус варианта ответа'
ANSWER_IS_CORRECT_HELP_TEXT = 'Укажите статус варианта ответа'
ANSWER_VERBOSE_NAME = 'Вариант ответа'
ANSWER_VERBOSE_NAME_PLURAL = 'Варианты ответов'

USER_ANSWER_USER_VERBOSE_NAME = 'Пользователь'
USER_ANSWER_QUESTION_VERBOSE_NAME = 'Вопрос'
USER_ANSWER_ANSWER_VERBOSE_NAME = 'Вариант ответа'
USER_ANSWER_VERBOSE_NAME = 'Ответ пользователя'
USER_ANSWER_VERBOSE_NAME_PLURAL = 'Ответы пользователей'

USER_QUIZ_RESULT_USER_VERBOSE_NAME = 'Пользователь'
USER_QUIZ_RESULT_QUIZ_VERBOSE_NAME = 'Тест'
USER_QUIZ_RESULT_RESULT_VERBOSE_NAME = 'Результат теста'
USER_QUIZ_RESULT_RESULT_HELP_TEXT = 'Укажите результат теста'
USER_QUIZ_RESULT_SUCCESS_STATUS_VERBOSE_NAME = 'Статус прохождения теста'
USER_QUIZ_RESULT_SUCCESS_STATUS_HELP_TEXT = 'Укажите статус прохождения теста'
USER_QUIZ_RESULT_VERBOSE_NAME = 'Результаты пользователя'
USER_QUIZ_RESULT_VERBOSE_NAME_PLURAL = 'Результаты пользователей'


class Quiz(models.Model):
    """Модель теста/квиза, привязанного к уроку.
    
    Attributes:
        title (str): Название теста
        lesson (Lesson): Урок, к которому привязан тест
        passing_score (int): Проходной балл для успешного завершения
    """

    title = models.CharField(
        QUIZ_TITLE_VERBOSE_NAME,
        max_length=QUIZ_TITLE_MAX_LENGTH,
        help_text=QUIZ_TITLE_HELP_TEXT
    )
    lesson = models.OneToOneField(
        'courses.Lesson',
        on_delete=models.CASCADE,
        verbose_name=QUIZ_LESSON_VERBOSE_NAME,
        related_name='quiz'
    )
    passing_score = models.PositiveBigIntegerField(
        QUIZ_PASSING_SCORE_VERBOSE_NAME,
        default=QUIZ_PASSING_SCORE_DEFAULT,
        help_text=QUIZ_PASSING_SCORE_HELP_TEXT
    )

    class Meta:
        verbose_name = QUIZ_VERBOSE_NAME
        verbose_name_plural = QUIZ_VERBOSE_NAME_PLURAL
        ordering = ['title', 'passing_score']

    def __str__(self):
        return self.title


class Question(models.Model):
    """Модель вопроса в тесте.
    
    Attributes:
        quiz (Quiz): Тест, к которому относится вопрос
        text (str): Текст вопроса
    """

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name=QUESTION_QUIZ_VERBOSE_NAME
    )
    text = models.TextField(
        QUESTION_TEXT_VERBOSE_NAME,
        help_text=QUESTION_TEXT_HELP_TEXT
    )

    class Meta:
        verbose_name = QUESTION_VERBOSE_NAME
        verbose_name_plural = QUESTION_VERBOSE_NAME_PLURAL
        ordering = ['quiz__title', 'text']
        default_related_name = '%(class)ss'

    def __str__(self):
        return f'{self.text[:30]}...'


class Answer(models.Model):
    """Модель варианта ответа на вопрос.
    
    Attributes:
        question (Question): Вопрос, к которому относится вариант
        text (str): Текст варианта ответа
        is_correct (bool): Является ли вариант правильным
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=ANSWER_QUESTION_VERBOSE_NAME
    )
    text = models.CharField(
        ANSWER_TEXT_VERBOSE_NAME,
        max_length=ANSWER_TEXT_MAX_LENGTH,
        help_text=ANSWER_TEXT_HELP_TEXT
    )
    is_correct = models.BooleanField(
        ANSWER_IS_CORRECT_VERBOSE_NAME,
        default=False,
        help_text=ANSWER_IS_CORRECT_HELP_TEXT
    )

    class Meta:
        verbose_name = ANSWER_VERBOSE_NAME
        verbose_name_plural = ANSWER_VERBOSE_NAME_PLURAL
        ordering = ['question__text', 'text']
        default_related_name = '%(class)ss'


class UserAnswer(models.Model):
    """Модель ответа пользователя на вопрос теста.
    
    Attributes:
        user (CustomUser): Пользователь, давший ответ
        question (Question): Вопрос теста
        answer (Answer): Выбранный вариант ответа
    """

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        verbose_name=USER_ANSWER_USER_VERBOSE_NAME
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=USER_ANSWER_QUESTION_VERBOSE_NAME
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name=USER_ANSWER_ANSWER_VERBOSE_NAME
    )

    class Meta:
        verbose_name = USER_ANSWER_VERBOSE_NAME
        verbose_name_plural = USER_ANSWER_VERBOSE_NAME_PLURAL
        ordering = ['user__email', 'question__text']
        default_related_name = '%(class)ss'

    def __str__(self):
        return f'{self.user.email}: {self.answer.text[:30]}...'


class UserQuizResult(models.Model):
    """Модель результата прохождения пользователем теста.
    
    Attributes:
        user (CustomUser): Пользователь, давший ответ
        quiz (Quiz): Тест
        result (int): баллы за тест
    """

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        verbose_name=USER_QUIZ_RESULT_USER_VERBOSE_NAME
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name=USER_QUIZ_RESULT_QUIZ_VERBOSE_NAME
    )
    score = models.PositiveIntegerField(
        USER_QUIZ_RESULT_RESULT_VERBOSE_NAME,
        help_text=USER_QUIZ_RESULT_RESULT_HELP_TEXT
    )
    success_status = models.BooleanField(
        USER_QUIZ_RESULT_SUCCESS_STATUS_VERBOSE_NAME,
        default=True,
        help_text=USER_QUIZ_RESULT_SUCCESS_STATUS_HELP_TEXT
    )

    class Meta:
        verbose_name = USER_QUIZ_RESULT_VERBOSE_NAME
        verbose_name_plural = USER_QUIZ_RESULT_VERBOSE_NAME_PLURAL
        default_related_name = 'user_quiz_results'
        ordering = ['user__email', 'quiz__title']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'quiz'],
                name='%(app_label)s_%(class)s_user_quiz_unique_together'
            )
        ]

    def __str__(self):
        return f'{self.user.email} - {self.result}'
