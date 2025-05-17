import os
import uuid
import ffmpeg
from celery import shared_task
from django.conf import settings
from products.models.product import Product

@shared_task
def process_video_task(product_id):
    try:
        instance = Product.objects.get(id=product_id)

        if not instance.video:
            return

        original_path = instance.video.path

        # Создание путей
        compressed_filename = f"compressed_{uuid.uuid4()}.mp4"
        compressed_path = os.path.join(settings.MEDIA_ROOT, 'compressed', compressed_filename)
        os.makedirs(os.path.dirname(compressed_path), exist_ok=True)

        # Сжатие видео
        try:
            (
                ffmpeg
                .input(original_path)
                .output(compressed_path, vcodec='libx264', crf=28)
                .run(capture_stdout=True, capture_stderr=True)
            )
            instance.video.name = f"compressed/{compressed_filename}"
        except Exception as e:
            print("Compression error:", e)

        # Генерация превью
        thumb_filename = f"thumb_{uuid.uuid4()}.jpg"
        thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', thumb_filename)
        os.makedirs(os.path.dirname(thumb_path), exist_ok=True)

        try:
            (
                ffmpeg
                .input(compressed_path, ss=1)
                .filter('scale', 320, -1)
                .output(thumb_path, vframes=1)
                .run(capture_stdout=True, capture_stderr=True)
            )
            instance.thumbnail.name = f"thumbnails/{thumb_filename}"
        except Exception as e:
            print("Thumbnail error:", e)

        instance.save()

    except Product.DoesNotExist:
        print(f"Product with ID {product_id} not found.")
