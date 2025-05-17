from rest_framework.routers import DefaultRouter
from .views.product_view import ProductViewSet
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
