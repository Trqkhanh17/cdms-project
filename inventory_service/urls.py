from django.urls import path
from inventory_service.views import ProductDetailAPIView, ProductListAPIView

PRODUCTS_PATH = "Products"

urlpatterns = [
    path(
        PRODUCTS_PATH,
        ProductListAPIView.as_view(),
        name="products-list",
    ),
    path(
        f"{PRODUCTS_PATH}/<int:product_id>",
        ProductDetailAPIView.as_view(),
        name="products-detail",
    ),
]
