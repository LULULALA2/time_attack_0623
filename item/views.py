from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from item.models import Item
from item.serializers import CategorySerializers, ItemSerializers, OrderSerializers, ItemOrderSerializers


# Create your views here.
class ItemView(APIView):
    def get(self, request):


        item_serialized_data = ItemSerializers(ata=request.data)
        return Response(item_serialized_data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['category_id'] = request.category.id
        item_serializer = ItemSerializers(data=request.data)
        if item_serializer.is_valid():
            item_serializer.save()
            return Response({"message": "저장"}, status=status.HTTP_200_OK)

        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

