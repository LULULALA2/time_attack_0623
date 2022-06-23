from rest_framework import serializers
from item.models import Category, Item, Order, ItemOrder

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemSerializers(serializers.ModelSerializer):
    # category = CategorySerializers() 이렇게 해도 되지만
    # output // "category": {"id":1, "name":food"}
    # 내가 원하는 대로 데이터를 편집해서 보여주기 위해서 아래처럼 SerializerMethodField()를 씀
    category = serializers.SerializerMethodField()
    # output // "category": "food"

    # 함수이름은 앞에 get_을 붙여야함
    # category의 name을 따로 빼서 category 필드에 넣어주기 위해서 이렇게 가져옴
    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Item
        fields = ["name", "category_id", "category", "image_url"]


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["delivery_address", "order_date"]


class ItemOrderSerializers(serializers.ModelSerializer):

    # order 모델의 내용도 불러오기 위해서 OrderSerializers 가져옴
    order = OrderSerializers(read_only=True) # order가 리스트로 되있으면 many=True 추가
    item_name = serializers.ReadOnlyField(source='item.name')
    # 모델 클래스 만들 듯, 시리얼라이즈에서 원래 모델에는 없는 새로운 attribute 'item_name'을 만들어줌
    # foreign_key로 item 모델에서 name을 가져오도록 source를 지정해줌

    class Meta:
        model = ItemOrder
        fields = ["id", "order", "item_name", "item_count"]
