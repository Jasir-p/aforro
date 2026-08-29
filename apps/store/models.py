from django.db import models
from apps.products.models import Products

# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        related_name="inventory"
        )

    product = models.ForeignKey(
        Products,
        on_delete=models.PROTECT,
        related_name='inventory'
    )

    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['store', 'product'],
                name='unique_store_item_inventory'
            )
        ]



    