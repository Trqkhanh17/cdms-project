from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cdms.excel_import import ExcelProductImporter
from cdms.serializers import ProductSnapshotSerializer
from cdms.serializers import ExcelUploadSerializer
from cdms.service import CdmsService
from cdms.scheduled_sync import ScheduledInventorySync
from common.api_exceptions import api_exception_handler


class ProductWebhookAPIView(APIView):
    @api_exception_handler
    def post(self, request):
        serializer = ProductSnapshotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        managed_product, changed = CdmsService().sync_product(serializer.validated_data)

        return Response(
            {
                "productId": managed_product.product_id,
                "changed": changed,
                "product": managed_product.product_data,
            },
            status=status.HTTP_200_OK,
        )


class ExcelProductUploadAPIView(APIView):
    @api_exception_handler
    def post(self, request):
        serializer = ExcelUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = ExcelProductImporter().import_file(
            serializer.validated_data["file"]
        )
        return Response(result, status=status.HTTP_200_OK)


class ScheduledSyncAPIView(APIView):
    @api_exception_handler
    def post(self, request):
        result = ScheduledInventorySync().run_once()
        return Response(result, status=status.HTTP_200_OK)
