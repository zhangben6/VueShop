from django.shortcuts import render
from .serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .models import Goods
# Create your views here.


# 写法1
# class GoodsListView(APIView):
#     """
#     List all goods, or create a new good.
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods, many=True)
#         return Response(goods_serializer.data)



# 写法2（更简洁)
# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     '''
#     商品列表页的展示
#     '''
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#
class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # 前端可通过这个参数进行动态返回数据
    page_query_param = 'p'
    max_page_size = 100

# 写法3  简直不要太爽  drf框架牛逼(实现了分页效果)
# class GoodsListView(generics.ListAPIView):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     # 设置分页的配置
#     pagination_class = GoodsPagination


# 写法4  飘了飘了  高速飙车中。。。
class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 设置分页的配置
    pagination_class = GoodsPagination