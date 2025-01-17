# Используем минимальный базовый образ Python
FROM python:3.13-slim

# Установим основные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установим Poetry
RUN pip install --no-cache-dir poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Скопируем только файлы, необходимые для установки зависимостей
COPY pyproject.toml poetry.lock /app/

# Установим зависимости через Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Скопируем всё остальное
COPY . /app/

# Удалим временные файлы
RUN find . -name '*.pyc' -delete && find . -name '__pycache__' -delete

# Открываем порт для приложения
EXPOSE 8500

# Команда запуска приложения
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8500"]
