from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins
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







