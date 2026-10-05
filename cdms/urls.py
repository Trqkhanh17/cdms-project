from django.urls import path

from cdms.views import (
    ExcelProductUploadAPIView,
    ProductWebhookAPIView,
    ScheduledSyncAPIView,
)


urlpatterns = [
    path(
        "webhooks/products",
        ProductWebhookAPIView.as_view(),
        name="product-webhook",
    ),
    path(
        "uploads/products",
        ExcelProductUploadAPIView.as_view(),
        name="product-excel-upload",
    ),
    path(
        "scheduled-sync",
        ScheduledSyncAPIView.as_view(),
        name="scheduled-sync",
    ),
]
