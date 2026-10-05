from rest_framework.response import Response
from rest_framework.views import APIView
from inventory_service.serializers import ProductSerializer
from inventory_service.service import ProductService

class ProductListAPIView(APIView):

    def get(self, request):
        products = ProductService().list_products()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data)
    

class ProductDetailAPIView(APIView):

    def get(self,request, product_id):
        product = ProductService().get_product(product_id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)