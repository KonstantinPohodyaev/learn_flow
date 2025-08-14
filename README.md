# 🎓 Learn Flow - Онлайн-платформа для курсов и тестов

![Django](https://img.shields.io/badge/Django-5.2.4-092E20?logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.5.3-ff6600?logo=python)
![Redis](https://img.shields.io/badge/Redis-7.2-DC382D?logo=redis)
![MySQL](https://img.shields.io/badge/MySQL-8.1-4479A1?logo=mysql)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?logo=docker)
![Nginx](https://img.shields.io/badge/Nginx-1.27-009639?logo=nginx)

> 🖥️ Платформа для размещения онлайн-курсов с тестами. После успешного прохождения всех тестов курса генерируется персональный диплом, который можно скачать или получить на email.

---

## 🚀 Основные возможности

### 🧩 Backend (Django + Celery + Redis)
- 📡 Продвинутая многоуровневая база данных MySQL
- 🔐 Авторизация и аутентификация пользователей:
  - Админ-панель для суперюзеров: создание/редактирование курсов, тестов, вопросов
  - Полный функционал доступен только авторизованным пользователям
- 📊 Оптимизированные запросы и работа с связанными моделями
- ✉️ Отправка писем в фоновом режиме (Celery + Redis)
- 🧠 Бизнес-логика:
  - FormSet для удобного создания вопросов с ответами
  - Автоматическое удаление файлов при удалении записей
  - Генерация уникальных сертификатов
  - Красивые шаблоны с адаптивным CSS

### ⚙️ Инфраструктура и DevOps
- 🐳 Docker + Docker Compose: простой запуск всех компонентов
- 🌐 Nginx: реверс-прокси для сайта
- 📂 Работа со статикой и медиа (сертификаты, CSS, картинки)
- 🔒 Контейнеризация для разделения ответственности между сервисами

---

## ⚙️ Установка

```bash
git clone https://github.com/KonstantinPohodyaev/learn_flow.git
cd learn_flow
```

Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
source venv/bin/activate  # Windows: . venv\Scripts\activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

### 📦 Переменные окружения

Создайте `.env` файл в корне проекта:

```env
# === DATABASE CONFIGURATION ===
DEBUG                            # Включение режима отладки
EMAIL_HOST                       # SMTP-сервер для отправки писем
EMAIL_PORT                       # Порт SMTP
EMAIL_USE_TLS                    # Включение TLS
EMAIL_HOST_USER                  # Почтовый ящик отправителя
EMAIL_HOST_PASSWORD.             # Пароль приложения Yandex
DEFAULT_FROM_EMAIL.              # Адрес отправителя по умолчанию

# Настройки MySQL
MYSQL_DATABASE=db                # Имя базы данных
MYSQL_USER=user                  # Пользователь базы
MYSQL_PASSWORD=password          # Пароль пользователя
MYSQL_ROOT_PASSWORD=rootpassword # Пароль root для MySQL
DB_HOST=db                       # Хост базы (контейнер Docker)
DB_PORT=3306                     # Порт базы данных

# Настройки Celery / Redis
CELERY_BROKER_URL=redis://redis:6379/0       # URL брокера для очередей задач
CELERY_RESULT_BACKEND=redis://redis:6379/0   # URL для хранения результатов задач
```
---

## ▶️ Запуск в отдельных терминалах для тестирования

### Выполнение Миграций
```bash
cd learn_flow
python manage.py migrate
```

## ▶️ Запуск в Docker-контейнерах
_Перед выполнением команды необходимо запустить Docker Desktop_

### Запуск контейнеров:
_В терминале перейти на уровень с файлом docker-compose.yml_

```bash
docker compose up -d
```

### Остановка контейнеров
```bash
docker compose down
```

_Сайт будет доступен по ```http://localhost```_

---

## 📌 Пример использования


---

## 👨‍💻 Автор

**Походяев Константин**  
Telegram: [@kspohodyaev](https://t.me/kspohodyaev)

---
