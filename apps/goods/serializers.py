# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/12 17:43'

# serializer.py文件的作用相对于django中的Form，将form表单实例化成html代码，
# 而serializer是将models对象转换成json序列化对象

from rest_framework import serializers

from goods.models import Goods,GoodsCategory


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        # fields = ('name','click_num','market_price','add_time')
        fields = "__all__"

# 类似于Django中ModelForm的写法
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Goods
        # fields = ('name','click_num','market_price','add_time')
        fields = "__all__"
