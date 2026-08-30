from rest_framework import serializers
from apps.products.models import Products

class ProductSearchSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    inventory_quantity = serializers.IntegerField(
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Products
        fields = ['id', 'title', 'description',
                  'price', "category_name",
                        "inventory_quantity"
                  ]