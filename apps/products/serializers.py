from .models import Category, Products
from rest_framework import serializers
import re
from decimal import Decimal



class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=50,
        error_messages={
            "blank": "Category name is required.",
            "max_length": "Category name cannot exceed 50 characters.",
        }
    )

    class Meta:
        model = Category
        fields = ["id", "name"]

    def validate_name(self, value):
        value = value.strip()

        if not re.fullmatch(r"[A-Za-z0-9 ]+", value):
            raise serializers.ValidationError(
                "Category name can contain only letters, numbers, and spaces."
            )

        # Check duplicate category names
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(
                "A category with this name already exists."
            )

        return value


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = [
            "id",
            "title",
            "description",
            "price",
            "category",
            "created_at"
        ]

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Product title cannot be blank"
            )

        return value

    def validate_price(self, value):
        if value <= Decimal("0"):

            raise serializers.ValidationError(
                "Price must be a valid"
            )

        return value

    def validate_description(self, value):
        return value.strip()

    
class ProductsListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Products
        fields = [
            "id",
            "title",
            "description",
            "price",
            "category",
            "created_at"
        ]