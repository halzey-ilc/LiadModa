from django.db import models

class Product(models.Model):
    STATUS_CHOICES = [
        ('pending', '⏳ В ожидании'),
        ('processing', '⚙️ Обработка'),
        ('done', '✅ Готово'),
        ('failed', '❌ Ошибка'),
    ]

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    whatsapp_number = models.CharField(max_length=20)

    video = models.URLField(max_length=500, blank=True, null=True)
    thumbnail = models.URLField(max_length=500, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
