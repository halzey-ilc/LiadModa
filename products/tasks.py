from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
import os
import uuid
from django.conf import settings
from src.utils.rust_video import compress_video
from products.models.product import Product
import ffmpeg


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
            print("❌ Rust-сжатие не удалось, задача будет повторена...")
            raise self.retry(
                countdown=15,
                exc=Exception("Rust compression failed")
            )

        instance.video.name = f"compressed/{compressed_filename}"

        # Превью
        thumb_filename = f"thumb_{uuid.uuid4()}.jpg"
        thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', thumb_filename)
        os.makedirs(os.path.dirname(thumb_path), exist_ok=True)

        (
            ffmpeg
            .input(compressed_path, ss=1)
            .filter('scale', 320, -1)
            .output(thumb_path, vframes=1)
            .run(capture_stdout=True, capture_stderr=True)
        )

        instance.thumbnail.name = f"thumbnails/{thumb_filename}"
        instance.status = 'done'
        instance.save()

    except Product.DoesNotExist:
        print(f"❌ Продукт ID {product_id} не найден.")
    except self.retry.exc:
        raise
    except Exception as exc:
        instance = Product.objects.filter(id=product_id).first()
        if instance:
            instance.status = 'failed'
            instance.save()
        print(f"🔥 Необрабатываемая ошибка: {exc}")
        raise exc
