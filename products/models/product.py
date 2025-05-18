import os
import uuid
from django.db import models
from django.utils.text import slugify

def video_upload_path(instance, filename):
    return f"videos/{uuid.uuid4()}_{slugify(filename)}"

def thumbnail_upload_path(instance, filename):
    return f"thumbnails/{uuid.uuid4()}_{slugify(filename)}"

class Product(models.Model):
    STATUS_CHOICES = [
        ('pending', ' В ожидании'),
        ('processing', ' Обработка'),
        ('done', ' Готово'),
        ('failed', ' Ошибка'),
    ]

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    whatsapp_number = models.CharField(max_length=20)
    video = models.FileField(upload_to=video_upload_path)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Только один раз указываем статус
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title
