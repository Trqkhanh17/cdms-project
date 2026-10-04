from inventory_service.views import ProductDetailAPIView
from django.urls import path
from inventory_service.views import ProductListAPIView

urlpatterns = [
    path('products',ProductListAPIView.as_view(), name='products-list'),
    path('product/<int:product_id>',ProductDetailAPIView.as_view(), name='products-detail')
]