# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/20 11:41'

import time

from .models import ShoppingCart
from rest_framework import serializers
from goods.models import Goods
from goods.serializers import GoodsSerializer
from .models import OrderInfo,OrderGoods,ShoppingCart
from utils.alipay import AliPay
from MxShop.settings import ali_pub_key_path,private_key_path


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


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    # 获取支付页面的url
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        # 此函数将生成支付宝支付页面的url
        alipay = AliPay(
            appid="2016093000631244",
            app_notify_url="http://120.78.170.188:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://120.78.170.188:8001/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,  # 支付对象
            out_trade_no=obj.order_sn,  # 订单号
            total_amount=obj.order_mount,  # 总金额
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url
    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # 生成订单的时候这些不用post，不能在前端进行修改
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    nonce_str = serializers.CharField(read_only=True)
    pay_type = serializers.CharField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self,obj):
        # 此函数将生成支付宝支付页面的url
        alipay = AliPay(
            appid="2016093000631244",
            app_notify_url="http://120.78.170.188:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://120.78.170.188:8001/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,   # 支付对象
            out_trade_no=obj.order_sn,  # 订单号
            total_amount=obj.order_mount, # 总金额
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    # 因为前端序列化的serializer没有订单号，需要在实例化对象save之前插入一段订单号
    def generate_order_sn(self):
        # 生成一个随机数
        from random import Random
        random_ins = Random()

        # 当前时间+user.id+随机数
        order_sn = '{time_str}{user_id}{ranstr}'.format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                        user_id=self.context['request'].user.id, ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self,attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


