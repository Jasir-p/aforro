from django.db import models
from apps.store.models import Store
from apps.products.models import Products

# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = [

        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("REJECTED", "Rejected"),
    ]
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        related_name="order"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.PROTECT,
        related_name='items'

    )
    quantity_requested = models.PositiveIntegerField()