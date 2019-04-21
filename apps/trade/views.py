from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins
from django.shortcuts import redirect
import time

from utils.permissions import IsOwnerOrReadOnly
from .serializer import ShopCartSerializer,ShopCartDetailSerializer,OrderSerializer
from .serializer import OrderDetailSerializer
from .models import ShoppingCart,OrderInfo,OrderGoods
# Create your views here.

class shoppingCartViewset(viewsets.ModelViewSet):
    '''
    购物车功能
    list:
        获取购物车详情
    create:
        加入购物车
    delete：
        删除购物记录
    '''
    # 用户的验证和权限验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 当拿到商品的id时，做商品的详情操作
    lookup_field = 'goods_id'

    # 根据不同http动作，序列化不同的serializer
    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    # 如果需要做list列表页功能，就需要重写get_queryset方法进行展示
    def get_queryset(self):
        '''
        返回当前用户购物车的列表
        :return:
        '''
        return ShoppingCart.objects.filter(user=self.request.user)



class OrderViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    '''
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create:
        新增订单
    '''
    # 用户的验证和权限验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()

        # 拿到order，生成对应的订单商品信息详情表
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)


from rest_framework.views import APIView
from utils.alipay import AliPay
from MxShop.settings import ali_pub_key_path,private_key_path
from datetime import datetime
from rest_framework.response import Response

class AlipayView(APIView):
    def get(self,request):
        '''
        处理支付宝的return_url返回
        :param request:
        :return:
        '''
        # 处理回调数据，跟之前的sign做比对
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)

        # 创建一个支付对象
        alipay = AliPay(
            appid="2016093000631244",
            app_notify_url="http://120.78.170.188:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://120.78.170.188:8001/alipay/return/"
        )

        # 进行回调参数的验证
        verify_re = alipay.verify(processed_dict, sign)

        # 这里可以不做操作。因为不管发不发return url。notify url都会修改订单状态。
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            # 支付宝会异步的给我们发送支付成功消息，需要回复success字符串
            response = redirect('index')
            response.set_cookie('nextPath','pay',max_age=3)  # 前端vue项目会识别到这些值做出相应操作
            return response
        else:
            # 支付信息被篡改的情况下，直接跳转到首页
            response = redirect('index')
            return response


    def post(self,request):
        '''
        处理支付宝的notify_url
        :param request:
        :return:
        '''

        # 处理回调数据，跟之前的sign做比对
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)

        # 创建一个支付对象
        alipay = AliPay(
            appid="2016093000631244",
            app_notify_url="http://120.78.170.188:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://120.78.170.188:8001/alipay/return/"
        )

        # 进行回调参数的验证
        verify_re = alipay.verify(processed_dict, sign)

        # 这里可以不做操作。因为不管发不发return url。notify url都会修改订单状态。
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            # 支付宝会异步的给我们发送支付成功消息，需要回复success字符串
            return Response('success')

        else:
            # 支付信息被篡改的情况下，直接跳转到首页
            response = redirect('index')
            return response






