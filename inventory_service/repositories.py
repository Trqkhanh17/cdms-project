from django.db.models import QuerySet

from inventory_service.models import Product


class ProductRepository:
    def list_products(self) -> QuerySet[Product]:
        return Product.objects.all()

    def get_product_by_id(self, product_id: int) -> Product | None:
        return Product.objects.filter(
            productId=product_id
        ).first()