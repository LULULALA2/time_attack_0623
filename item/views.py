from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from item.models import Item, Category, ItemOrder
from item.serializers import ItemSerializers, ItemOrderSerializers


class ItemView(APIView):
    def get(self, request):
        # 1) 프론트에서 body에 json으로 보낸 데이터 가져올때
        # category = request.data['category'] - 카테고리가 없으면 keyerror 남
        # category = request.data.get('category', None) - 카테고리가 없어도 none으로 에러없을 수 있음

        # 2) (프론트 url)쿼리스트링으로 데이터 가져올 때
        category = request.GET.get('category', None)
        # category = self.request.query_params.get('category')
        # 프론트에서 category값이 아무것도 안들어왔을 때, none 값을 넣어줌

        items = Item.objects.filter(category__name=category) # 카테고리 이름으로 검색하도록 조건
        # items = Category.objects.prefetch_related('item_set').get(name=category).item_set.all()

        # prefetch_related :
        # item_set : Category에서 Item을 역참조할 때 이름
        #           (이름을 바꿔주려면 Item.category의 related_name 설정)


        if items.exists(): # 있는 카테고리일때
            item_serializer = ItemSerializers(items, many=True)
            # 위에서 조건검색으로 가져온 items(쿼리셋)를 ItemSerializers에 넣어서 직렬화 시켜줌
            return Response(item_serializer.data, status=status.HTTP_200_OK)
            # 직렬화된 데이터에 .data 를 붙여서 json 형식으로 바꿔줌

        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # 프론트에서 받아온 데이터를 시리얼라이저에 넣어줌
        item_serializer = ItemSerializers(data=request.data) # data 키가 있으면 serializer안에

        # POST할때, 데이터검증(validation)하고 db에 저장해야함
        if item_serializer.is_valid():
            # 프론트에서 쿼리스트링으로 가져온 category_id 를 Category에서 찾아서
            # 있으면 get_object / 없으면 HTTP_404_NOT_FOUND 에러 발생시킴
            category_instance = get_object_or_404(Category, id=request.data['category'])

            # item의 category에 가져온 category 객체를 넣어줘서 category_id를 채워줌
            # (CategorySerializers를 ItemSerializers에 넣어줄때 name만 가져왔기 때문에)
            item_serializer.save(category=category_instance)  # item의 category 임!

            # 만약 ItemSerializers에 category = CategorySerializers()해서 category를
            # 통째로 넣었다면 그냥 item_serializer.save() 해도 됨 (category_id가 이미 들어있어서)

            # custom serializer create
            return Response({"message":"저장완료!"}, status=status.HTTP_200_OK)

        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemOrderView(APIView):
    def get(self, request):
        order_id = self.request.query_params.get('order_id')

        data = ItemOrder.objects.filter(
            Q(order__order_date__range=[timezone.now() - timedelta(days=7), timezone.now()]) &
            Q(order_id=order_id)
        )

        if data.exists():
            serializer = ItemOrderSerializers(data, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)