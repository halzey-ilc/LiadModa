from rest_framework import serializers
from products.models.product import Product
from products.services.whatsapp import generate_whatsapp_link


class ProductSerializer(serializers.ModelSerializer):
    whatsapp_link = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['thumbnail', 'created_at']

    def validate_video(self, value):
        if value.size > 100 * 1024 * 1024:  # 100 MB
            raise serializers.ValidationError("Видео слишком большое (макс. 100МБ).")
        if not value.name.lower().endswith(('.mp4', '.mov', '.avi')):
            raise serializers.ValidationError("Разрешены только .mp4, .mov, .avi форматы.")
        return value

    def get_whatsapp_link(self, obj):
        return generate_whatsapp_link(obj.whatsapp_number, obj.title)
