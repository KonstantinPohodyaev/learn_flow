from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

EMAIL_VERBOSE_NAME = 'Почта'
EMAIL_HELP_TEXT = 'Введите почту'

FULL_NAME_VERBOSE_NAME = 'Полное имя'
FULL_NAME_MAX_LENGTH = 255

IS_ACTIVE_VERBOSE_NAME = 'Статус активности'
IS_STAFF_VERBOSE_NAME = 'Статус сотрудника'

VK_ID_VERBOSE_NAME = 'Уникальный идентификатор Вконтакте'
VK_ID_MAX_LENGTH = 63

CUSTOM_USER_VERBOSE_NAME = 'Пользователь'
CUSTOM_USER_VERBOSE_NAME_PLURAL = 'Пользователи'


class CustomUserManager(BaseUserManager):
    """Кастоный менеджер записей для модели CustomUser."""

    def create_user(self, email, password=None, **extra_fields):
        """Кастомный метод создания пользователя."""
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        EMAIL_VERBOSE_NAME,
        unique=True,
        help_text=EMAIL_HELP_TEXT
    )
    full_name = models.CharField(
        FULL_NAME_VERBOSE_NAME,
        max_length=FULL_NAME_MAX_LENGTH
    )
    is_active = models.BooleanField(IS_ACTIVE_VERBOSE_NAME, default=True)
    is_staff = models.BooleanField(IS_STAFF_VERBOSE_NAME, default=False)
    vk_id = models.CharField(
        VK_ID_VERBOSE_NAME,
        max_length=VK_ID_MAX_LENGTH,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = CUSTOM_USER_VERBOSE_NAME
        verbose_name_plural = CUSTOM_USER_VERBOSE_NAME_PLURAL
        ordering = ['full_name', 'email']