from django.shortcuts import render
from rest_framework import views, response, status, permissions
from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderDetailserializer
from .services import create_order, get_store_orders
from drf_spectacular.utils import extend_schema,OpenApiParameter
# Create your views here.



class OrderCreateView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Create Order",
        description=(
            "Create an order for a store. "
            "The order is CONFIRMED when sufficient inventory "
            "is available, otherwise it is REJECTED."
        ),
        request=OrderCreateSerializer,
        responses={201: OrderDetailserializer},
    )
    def post(self, request):

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(
            raise_exception=True
        )

        order = create_order(
            store_id=serializer.validated_data["store_id"],
            items=serializer.validated_data["items"]
        )
        response_serializer = OrderDetailserializer(order)


        return response.Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class OrdersListView(views.APIView):
     
    permission_classes = [permissions.AllowAny]
    @extend_schema(
        summary="List Orders",
        description="Get orders, optionally filtered by store.",
        parameters=[
            OpenApiParameter(
                name="store_id",
                type=int,
                required=False,
                description="Filter orders by store ID",
            ),
        ],
        responses={200: OrderDetailserializer(many=True)},
    )
    def get(self, request, store_id):

        orders = get_store_orders(store_id)

        serializer = OrderDetailserializer(orders, many=True)

        return response.Response(
            serializer.data,
            status=status.HTTP_200_OK
        )