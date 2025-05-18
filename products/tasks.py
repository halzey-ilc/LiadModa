from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
import os
import uuid
import ffmpeg
from django.conf import settings
from src.utils.rust_video import compress_video
from src.utils.cloudinary_utils import upload_to_cloudinary
from products.models.product import Product


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def process_video_task(self, product_id):
    try:
        instance = Product.objects.get(id=product_id)

        if not instance.video:
            instance.status = 'failed'
            instance.save()
            print("⚠️ Нет видео у продукта.")
            return

        instance.status = 'processing'
        instance.save()

        original_path = instance.video.path

        # Сжатие
        compressed_filename = f"compressed_{uuid.uuid4()}.mp4"
        compressed_path = os.path.join(settings.MEDIA_ROOT, 'compressed', compressed_filename)
        os.makedirs(os.path.dirname(compressed_path), exist_ok=True)

        success = compress_video(original_path, compressed_path)
        if not success:
            instance.status = 'failed'
            instance.save()
            raise self.retry(
                countdown=15,
                exc=Exception("Rust compression failed")
            )

        # ✅ Загрузка видео на Cloudinary
        cloud_video_url = upload_to_cloudinary(compressed_path, folder='videos', resource_type='video')
        instance.video = cloud_video_url

        # Генерация превью
        thumb_filename = f"thumb_{uuid.uuid4()}.jpg"
        thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', thumb_filename)
        os.makedirs(os.path.dirname(thumb_path), exist_ok=True)

        ffmpeg.input(compressed_path, ss=1).filter('scale', 320, -1).output(
            thumb_path, vframes=1).run(capture_stdout=True, capture_stderr=True)

        # ✅ Загрузка превью на Cloudinary
        cloud_thumb_url = upload_to_cloudinary(thumb_path, folder='thumbnails', resource_type='image')
        instance.thumbnail = cloud_thumb_url

        instance.status = 'done'
        instance.save()

        # Удаляем временные файлы
        os.remove(compressed_path)
        os.remove(thumb_path)

    except Product.DoesNotExist:
        print(f" Продукт ID {product_id} не найден.")
    except self.retry.exc:
        raise
    except Exception as exc:
        instance = Product.objects.filter(id=product_id).first()
        if instance:
            instance.status = 'failed'
            instance.save()
        print(f"🔥 Необрабатываемая ошибка: {exc}")
        raise exc
