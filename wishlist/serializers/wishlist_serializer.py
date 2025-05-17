from rest_framework import serializers
from wishlist.models.wishlist import Wishlist
from products.models.product import Product
from products.serializers.product_serializer import ProductSerializer

class WishlistSerializer(serializers.ModelSerializer):
    # 🔹 это поле для GET-запросов — оно вложенное, читабельное
    product = ProductSerializer(read_only=True)
    # 🔹 это поле только для POST — оно получает ID товара
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_id', 'added_at']
