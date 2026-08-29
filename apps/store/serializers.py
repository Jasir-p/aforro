from rest_framework import serializers, validators
from .models import Store, Inventory


class StoreSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        validators=[
            validators.UniqueValidator(
                queryset=Store.objects.all(),
                message="A store with name already registerd"
            )
        ]
    )

    class Meta:
        model = Store
        fields = ["id", "name", "location"]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "store name cannot be null"
            )

        return value

    def validate_location(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "location field cannot be null"
            )

        return value


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ['id', 'store', 'product', 'quantity']

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Please enter valid quantity number"
            )

        return value


class InventoryListSerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source="product.title",
        read_only=True

    )
    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    category_name = serializers.CharField(
        source="product.category.name",
        read_only=True
    )

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product_title",
            "price",
            "category_name",
            "quantity"
        ]