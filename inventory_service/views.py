from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from inventory_service.serializers import (
    ProductSerializer,
    ProductCreateAndUpdateSerializer,
)
from inventory_service.clients.cdms_webhook_client import CdmsWebhookClient
from inventory_service.service import ProductService
from common.api_exceptions import api_exception_handler


class ProductListAPIView(APIView):
    def get(self, request):
        products = ProductService().list_products()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data)

    @api_exception_handler
    def post(self, request):
        input_serializer = ProductCreateAndUpdateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        product = ProductService().create_product(input_serializer.validated_data)
        output_serializer = ProductSerializer(product)
        CdmsWebhookClient().send_product(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    def get(self, request, product_id):
        product = ProductService().get_product(product_id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @api_exception_handler
    def put(self, request, product_id):
        service = ProductService()
        product = service.get_product(product_id=product_id)
        input_serializer = ProductCreateAndUpdateSerializer(
            instance=product, data=request.data
        )
        input_serializer.is_valid(raise_exception=True)
        update_product = service.update_product(
            product, product_data=input_serializer.validated_data
        )
        output_serializer = ProductSerializer(update_product)
        CdmsWebhookClient().send_product(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
