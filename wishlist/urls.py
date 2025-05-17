from rest_framework.routers import DefaultRouter
from wishlist.views.wishlist_view import WishlistViewSet

router = DefaultRouter()
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = router.urls
