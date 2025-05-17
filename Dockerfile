# Используем официальный образ Python
FROM python:3.11

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда запуска (используем gunicorn как в Procfile)
CMD ["gunicorn", "videoshop_backend.wsgi", "--bind", "0.0.0.0:8000"]
