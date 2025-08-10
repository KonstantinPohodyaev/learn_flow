import os

from django.db import models

COURSE_TITLE_VERBOSE_NAME = 'Название курса'
COURSE_TITLE_MAX_LENGTH = 127
COURSE_TITLE_HELP_TEXT = 'Введите название курса'
COURSE_DESCRIPTION_VERBOSE_NAME = 'Описание курса'
COURSE_DESCRIPTION_HELP_TEXT = 'Укажите описание курса'
COURSE_OWNER_VERBOSE_NAME = 'Создатель курса'
COURSE_IS_PUBLISHED_VERBOSE_NAME = 'Для публикации'
COURSE_IS_PUBLISHED_HELP_TEXT = 'Укажите статус курса'
COURSE_VERBOSE_NAME = 'Курс'
COURSE_VERBOSE_NAME_PLURAL = 'Курсы'

MODULE_TITLE_VERBOSE_NAME = 'Название модуля'
MODULE_TITLE_MAX_LENGTH = 127
MODULE_TITLE_HELP_TEXT = 'Введите название модуля'
MODULE_COURSE_VERBOSE_NAME = 'Курс'
MODULE_VERBOSE_NAME = 'Модуль'
MODULE_VERBOSE_NAME_PLURAL = 'Модули'

LESSON_MODULE_VERBOSE_NAME = 'Модуль'
LESSON_TITLE_VERBOSE_NAME = 'Название урока'
LESSON_TITLE_MAX_LENGTH = 127
LESSON_TITLE_HELP_TEXT = 'Введите название урока'
LESSON_CONTENT_VERBOSE_NAME = 'Содержание урока'
LESSON_CONTENT_HELP_TEXT = 'Добавьте содержание урока'
LESSON_VIDEO_URL_VERBOSE_NAME = 'Ссылка на занятие'
LESSON_VIDEO_URL_HELP_TEXT = 'Добавьте ссылку на занятие'
LESSON_FILE_VERBOSE_NAME = 'Файл к уроку'
LESSON_FILE_HELP_TEXT = 'Прикрепите файл к уроку'
LESSON_VERBOSE_NAME = 'Урок'
LESSON_VERBOSE_NAME_PLURAL = 'Уроки'

COURSE_PROGRESS_USER_VERBOSE_NAME = 'Пользователь'
COURSE_PROGRESS_COURSE_VERBOSE_NAME = 'Курс'
COURSE_PROGRESS_LESSON_VERBOSE_NAME = 'Урок'
COURSE_PROGRESS_COMPLETED_VERBOSE_NAME = 'Статус курса'
COURSE_PROGRESS_COMPLETED_HELP_TEXT = 'Укажите статус курса'
COURSE_PROGRESS_VERBOSE_NAME = 'Прогресс курса'
COURSE_PROGRESS_VERBOSE_NAME_PLURAL = 'Прогресс курсов'

CERTIFICATE_USER_VERBOSE_NAME = 'Пользователь'
CERTIFICATE_COURSE_VERBOSE_NAME = 'Курс'
CERTIFICATE_FILE_VERBOSE_NAME = 'Файл диплома'
CERTIFICATE_VERBOSE_NAME = 'Сертификат'
CERTIFICATE_VERBOSE_NAME_PLURAL = 'Сертификаты'


class Course(models.Model):
    """Модель курса.

    Атрибуты:
        title (CharField): Название курса.
        description (TextField): Описание курса.
        owner (ForeignKey): Создатель курса (связь с пользователем).
        is_published (BooleanField): Статус публикации курса.
    """

    title = models.CharField(
        COURSE_TITLE_VERBOSE_NAME,
        max_length=COURSE_TITLE_MAX_LENGTH,
        help_text=COURSE_TITLE_HELP_TEXT
    )
    description = models.TextField(
        COURSE_DESCRIPTION_VERBOSE_NAME,
        help_text=COURSE_DESCRIPTION_HELP_TEXT
    )
    owner = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        verbose_name=COURSE_OWNER_VERBOSE_NAME
    )
    is_published = models.BooleanField(
        COURSE_IS_PUBLISHED_VERBOSE_NAME,
        default=False,
        help_text=COURSE_IS_PUBLISHED_HELP_TEXT
    )

    class Meta:
        verbose_name = COURSE_VERBOSE_NAME
        verbose_name_plural = COURSE_VERBOSE_NAME_PLURAL
        ordering = ['title', 'description']
        default_related_name = 'courses'

    def __str__(self):
        return f'{self.title }: {self.description[:30]}...'


class Module(models.Model):
    """Модель модуля курса.

    Attributes:
        title (CharField): Название модуля.
        course (ForeignKey): Курс, к которому относится модуль.
    """

    title = models.CharField(
        MODULE_TITLE_VERBOSE_NAME,
        max_length=MODULE_TITLE_MAX_LENGTH,
        help_text=MODULE_TITLE_HELP_TEXT
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=MODULE_COURSE_VERBOSE_NAME
    )

    class Meta:
        verbose_name = MODULE_VERBOSE_NAME
        verbose_name_plural = MODULE_VERBOSE_NAME_PLURAL
        default_related_name = 'modules'
        ordering = ['title', 'course__title']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока в модуле.

    Attributes:
        module (ForeignKey): Модуль, к которому относится урок.
        title (CharField): Название урока.
        content (TextField): Содержание урока.
        video_url (URLField): Ссылка на видео (опционально).
        file (FileField): Прикрепленный файл (опционально).
    """

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        verbose_name=LESSON_MODULE_VERBOSE_NAME
    )
    title = models.CharField(
        LESSON_TITLE_VERBOSE_NAME,
        max_length=LESSON_TITLE_MAX_LENGTH,
        help_text=LESSON_TITLE_HELP_TEXT
    )
    content = models.TextField(
        LESSON_CONTENT_VERBOSE_NAME,
        help_text=LESSON_CONTENT_HELP_TEXT
    )
    video_url = models.URLField(
        LESSON_VIDEO_URL_VERBOSE_NAME,
        blank=True,
        null=True,
        help_text=LESSON_VIDEO_URL_HELP_TEXT
    )
    file = models.FileField(
        LESSON_FILE_VERBOSE_NAME,
        upload_to='lessons/',
        blank=True,
        null=True,
        help_text=LESSON_FILE_HELP_TEXT
    )

    class Meta:
        verbose_name = LESSON_VERBOSE_NAME
        verbose_name_plural = LESSON_VERBOSE_NAME_PLURAL
        ordering = ['title', 'content']
        default_related_name = 'lessons'

    def __str__(self):
        return f'{self.title}: {self.content[:30]}...'


class CourseProgress(models.Model):
    """Модель для отслеживания прогресса пользователя по курсу.
    
    Attributes:
        user (CustomUser): Пользователь, проходящий курс
        course (Course): Курс, по которому отслеживается прогресс
        current_lesson (Lesson): Текущий урок, на котором находится пользователь
        completed (bool): Флаг завершения курса
    """

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        verbose_name=COURSE_PROGRESS_USER_VERBOSE_NAME
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=COURSE_PROGRESS_COURSE_VERBOSE_NAME
    )
    current_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name=COURSE_PROGRESS_LESSON_VERBOSE_NAME
    )
    completed = models.BooleanField(
        COURSE_PROGRESS_COMPLETED_VERBOSE_NAME,
        default=False,
        help_text=COURSE_PROGRESS_COMPLETED_HELP_TEXT
    )

    class Meta:
        verbose_name = COURSE_PROGRESS_VERBOSE_NAME
        verbose_name_plural = COURSE_PROGRESS_VERBOSE_NAME_PLURAL
        default_related_name = '%(class)ss'
        ordering = ['user__email', 'course__title']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='%(app_label)s_%(class)s_user_course_unique_together'
            )
        ]

    def __str__(self):
        return (
            f'{self.user.email}: {self.course.title}'
            f' - {self.current_lesson.title}'
        )


class Certificate(models.Model):
    """Модель сертификата о прохождении курса.
    
    Attributes:
        user (CustomUser): Пользователь, получивший сертификат
        course (Course): Курс, за который выдан сертификат
        file (File): Файл сертификата
    """

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        verbose_name=CERTIFICATE_USER_VERBOSE_NAME
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=CERTIFICATE_COURSE_VERBOSE_NAME
    )
    file = models.FileField(
        CERTIFICATE_FILE_VERBOSE_NAME,
        upload_to='certificates/'
    )

    class Meta:
        verbose_name = CERTIFICATE_VERBOSE_NAME
        verbose_name_plural = CERTIFICATE_VERBOSE_NAME_PLURAL
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='%(app_label)s_%(class)s_user_course_unique_together'
            )
        ]

    def __str__(self):
        return self.file.name


    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
