from inventory_service.models import Product
from django.contrib import admin



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "productId",
        "productName",
        "sku",
        "color",
        "size",
        "isActive",
    )

    search_fields = (
        "productName",
        "sku",
    )

    list_filter = (
        "isActive",
        "color",
        "size",
    )

    ordering = (
        "productId",
    )