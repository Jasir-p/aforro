from django.shortcuts import render
from rest_framework import views, response, status, permissions
from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderDetailserializer
from .services import create_order, get_store_orders
# Create your views here.



class OrderCreateView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):

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

    def get(self, request, store_id):

        orders = get_store_orders(store_id)

        serializer = OrderDetailserializer(orders, many=True)

        return response.Response(
            serializer.data,
            status=status.HTTP_200_OK
        )