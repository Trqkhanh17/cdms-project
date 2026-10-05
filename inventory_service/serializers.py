from rest_framework import serializers 
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["productId","productName","sku","color","size","isActive"]
        read_only_fields = ['productId']

class ProductCreateAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["productName","sku","color","size","isActive"]
