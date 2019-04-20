from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .serializer import ShopCartSerializer,ShopCartDetailSerializer
from .models import ShoppingCart
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












