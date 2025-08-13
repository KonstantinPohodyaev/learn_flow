FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/learn_flow

RUN mkdir -p /vol/backend/media /vol/backend/static
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "learn_flow.wsgi:application", "--bind", "0.0.0.0:8000"]