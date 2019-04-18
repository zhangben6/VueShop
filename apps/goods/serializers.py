# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/12 17:43'

# serializer.py文件的作用相对于django中的Form，将form表单实例化成html代码，
# 而serializer是将models对象转换成json序列化对象

from rest_framework import serializers

from goods.models import Goods,GoodsCategory
from .models import GoodsImage

# 类似于Django中Form的写法
# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data): # 为view中的save做铺垫
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Goods.objects.create(**validated_data)

class CategorySerializer3(serializers.ModelSerializer):
    '''
      商品类别序列化
      '''
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class CategorySerializer2(serializers.ModelSerializer):
    '''
      商品类别序列化
      '''
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    '''
      商品类别序列化
      '''
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)


# 类似于Django中ModelForm的写法
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        # fields = ('name','click_num','market_price','add_time')
        fields = "__all__"





