# Используем подходящий Python-образ (версии 3.9+, 3.10+ и т.д.)
FROM python:3.13-slim

# Отключаем генерацию pyc-файлов и буферизацию вывода Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаем директорию приложения внутри контейнера и переходим в нее
WORKDIR /app

# Устанавливаем Poetry, копируем pyproject.toml и poetry.lock, затем ставим зависимости
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root --no-interaction --no-ansi

# Копируем оставшийся код в контейнер
COPY . /app

# По желанию (если нужны статики внутри контейнера):
# RUN python HomeCenter/manage.py collectstatic --noinput

EXPOSE 8000
WORKDIR /app/HomeCenter
# Запускаем Uvicorn на 0.0.0.0:8000 c 1 воркером
CMD ["poetry", "run", "gunicorn", "HomeCenter.wsgi:application", "-w", "1", "--bind", "0.0.0.0:8000"]
