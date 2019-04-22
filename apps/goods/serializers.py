# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/12 17:43'

# serializer.py文件的作用相对于django中的Form，将form表单实例化成html代码，
# 而serializer是将models对象转换成json序列化对象

from rest_framework import serializers
from django.db.models import Q

from goods.models import Goods,GoodsCategory
from .models import GoodsImage,Banner,HotSearchWords,IndexAd,GoodsCategoryBrand

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


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class GoodSerializer1(serializers.ModelSerializer):
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = ['id','images']

class IndexCategorySerializer(serializers.ModelSerializer):
    # 取出与商品关联的brand图
    brands = BrandSerializer(many=True)

    # 取出一级商品中所有的子类商品
    goods = serializers.SerializerMethodField()
    def get_goods(self,obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods,many=True,context={'request':self.context['request']})
        return goods_serializer.data

    # 取出二级商品分类
    sub_cat = CategorySerializer2(many=True)

    # 取出广告位的商品
    ad_goods = serializers.SerializerMethodField()
    def get_ad_goods(self,obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            # 拿到goods对象后做序列化操作
            goods_json = GoodsSerializer(good_ins,many=False,context={'request':self.context['request']}).data
        return goods_json


    class Meta:
        model = GoodsCategory
        fields = "__all__"

