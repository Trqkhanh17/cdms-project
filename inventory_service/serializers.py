from rest_framework.fields import ReadOnlyField
from rest_framework import serializers 
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "productId",
            "productName",
            "sku",
            "color",
            "size",
            "isActive"
        ]
        read_only_fields = ['ProductId']