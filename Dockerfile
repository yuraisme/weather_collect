# Используем минимальный образ с предустановленным uv
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim as builder

# Устанавливаем только необходимые пакеты в одном слое
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только необходимые файлы (исключаем временные и большие файлы)
COPY requirements.txt .env ./
COPY HomeCenter HomeCenter/
COPY manage.py .

#RUN uv venv
RUN uv sync

# Финальный минимальный образ
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app
COPY --from=builder /app/ .

# Удаляем ненужные файлы и кэш
RUN find /app -name "*.pyc" -delete && \
    find /app -name "__pycache__" -type d -exec rm -rf {} +

EXPOSE 8000
WORKDIR /app/HomeCenter