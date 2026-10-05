from rest_framework import serializers


class ProductSnapshotSerializer(serializers.Serializer):
    productId = serializers.IntegerField()

    productName = serializers.CharField(
        max_length=255,
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    sku = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    color = serializers.CharField(
        max_length=50,
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    size = serializers.CharField(
        max_length=50,
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    isActive = serializers.BooleanField(required=False)


class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
