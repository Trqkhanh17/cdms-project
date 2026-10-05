from cdms.models import ManagedProduct


class ManagedProductRepository:
    def get_by_product_id(
        self,
        product_id: int,
    ) -> ManagedProduct | None:
        return ManagedProduct.objects.filter(product_id=product_id).first()

    def get_by_product_id_for_update(
        self,
        product_id: int,
    ) -> ManagedProduct | None:
        return ManagedProduct.objects.select_for_update().filter(
            product_id=product_id
        ).first()

    def create(
        self,
        product_id: int,
        product_data: dict,
    ) -> ManagedProduct:
        return ManagedProduct.objects.create(
            product_id=product_id,
            product_data=product_data,
        )

    def update(
        self,
        managed_product: ManagedProduct,
        product_data: dict,
    ) -> ManagedProduct:
        managed_product.product_data = product_data
        managed_product.save()
        return managed_product
