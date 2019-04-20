# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/20 11:41'

import time

from .models import ShoppingCart
from rest_framework import serializers
from goods.models import Goods
from goods.serializers import GoodsSerializer
from .models import OrderInfo,OrderGoods,ShoppingCart

class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False,read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('goods','nums')




class ShopCartSerializer(serializers.Serializer):
    #获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量",min_value=1,
                                    error_messages={
                                        "min_value":"商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    })
    #这里是继承Serializer，必须指定queryset对象，如果继承ModelSerializer则不需要指定
    #goods是一个外键，可以通过这方法获取goods object中所有的值
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    #继承的Serializer没有save功能，必须写一个create方法
    def create(self, validated_data):
        # validated_data是已经处理过的数据
        #获取当前用户
        # view中:self.request.user；serializer中:self.context["request"].user
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        #如果购物车中有记录，数量+1
        #如果购物车车没有记录，就创建
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            #添加到购物车
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
            # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance