import os
from rest_framework import viewsets
from products.models.product import Product
from products.serializers.product_serializer import ProductSerializer
from products.tasks import process_video_task  # Celery task
from rest_framework.parsers import MultiPartParser, FormParser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        instance = serializer.save(status='processing')  # 👈 устанавливаем статус при создании

        if instance.video:
            process_video_task.delay(instance.id)  # асинхронно сжимаем и делаем превью
       