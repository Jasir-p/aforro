from django.shortcuts import render
from rest_framework import views, viewsets,permissions,response,status
from .models import Store, Inventory
from .serializers import StoreSerializer, InventorySerializer, InventoryListSerializer

# Create your views here.


class StoreViews(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()



class InventoryCreateViews(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = InventorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return response.Response({"message": "successfull Addded"}, status=status.HTTP_201_CREATED)

        return response.Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class InventoryListView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request,*args, **kwargs):

        store_id = self.kwargs["store_id"]

        inventory_data = Inventory.objects.filter(
            store=store_id
        ).select_related(
            'product',
            'product__category'
        )

        serializer = InventoryListSerializer(inventory_data, many=True)

        return response.Response(serializer.data,status=status.HTTP_200_OK)