# Dockerfile
FROM python:3.9-slim-bullseye

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt сначала для кэширования
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем папки для статики и медиа
RUN mkdir -p static staticfiles

# Запускаем сервер с автоматическими миграциями
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]