from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .models import UserFav,UserLeavingMessage
from .serializer import UserFavSerializer,UserFavDetailSerializer
from utils.permissions import IsOwnerOrReadOnly
from .serializer import LeavingMessageSerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
# Create your views here.

class UserFavViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    '''
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    '''
     # 两个权限验证分别为是否登陆、是否为某一个用户
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    lookup_field = "goods_id"
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # 重载get_serializer_class,根据具体需求重载具体的serializer
    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer  # 默认返回

class LeavingMessageViewset(mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    '''
    list:
        获取用户留言
    create:
        添加留言
    delete：
        删除留言功能
    '''

    # 用户的验证和权限验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)