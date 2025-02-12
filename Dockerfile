# Используем готовый образ с установленным uv
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*
# Устанавливаем рабочую директорию
WORKDIR /app
# Копируем файлы проекта
COPY . /app
# RUN uv venv
RUN uv sync

# Открываем порт для Gunicorn
EXPOSE 8000
WORKDIR /app/HomeCenter

# коллекционируем для nginx
#RUN uv run python manage.py collectstatic 

# Команда запуска контейнера
# CMD ["uv", "run", "gunicorn", "HomeCenter.wsgi:application", "-w", "2", "--bind", "0.0.0.0:8000", "--log-level", "DEBUG"]
# CMD ["uv", "run", "python3", "manage.py", "runserver"]
# CMD ["uv", "run", "python3"]
