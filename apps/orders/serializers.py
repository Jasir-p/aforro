from rest_framework import serializers,validators
from .models import Order,OrderItem
from apps.store.models import Store




class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity_requested = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    store_id = serializers.IntegerField()
    items = OrderItemCreateSerializer(many=True)

    def validate_store_id(self, value):

        if not Store.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Store does not exist."
            )

        return value
    


class OrderDetailserializer(serializers.ModelSerializer):
    total_items = serializers.IntegerField(read_only=True)
    class Meta:
        model = Order
        fields = [
            "id",
            "store",
            "status",
            "created_at",
            "total_items"
        ]


