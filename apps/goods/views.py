from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from .models import Goods,GoodsCategory
from .filters import GoodsFilter
from .serializers import GoodsSerializer,CategorySerializer

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
    page_size = 12
    page_size_query_param = 'page_size'  # 前端可通过这个参数进行动态返回数据
    page_query_param = 'page'
    max_page_size = 100

# 写法3  简直不要太爽  drf框架牛逼(实现了分页效果)   官网一般用这种写法!但是urls.py中配置不一样
# class GoodsListView(generics.ListAPIView):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     # 设置分页的配置
#     pagination_class = GoodsPagination


# 写法4  飘了飘了  高速飙车中。。。
# class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     # 设置分页的配置
#     pagination_class = GoodsPagination
#

# ---------------------------------------------------------------------------------------------------------------------
#  drf的过滤器
# 写法1（根据判断request.query_param参数进行过滤)
# class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
#     queryset = Goods.objects.all()
#
#     serializer_class = GoodsSerializer
#     # 设置分页的配置
#     pagination_class = GoodsPagination
#
#     def get_queryset(self):
#         '''此函数位于genericViewSet类中的过滤函数'''
#         queryset = self.queryset
#         price_min = self.request.query_params.get('price_min',0)
#         if price_min:
#             queryset = queryset.filter(shop_price__gt=int(price_min))
#         return queryset



# 写法2 （根据django_filter_bankends)  准确值查找
# class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     # 设置分页的配置
#     pagination_class = GoodsPagination
#     filter_backends = (DjangoFilterBackend,)
#     filter_fields = ('name', 'shop_price')

# 写法3 自定义查找规则，引入filter_class,当然也到了模糊查询的字段功能
# class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     # 设置分页的配置
#     pagination_class = GoodsPagination
#     filter_backends = (DjangoFilterBackend,)
#     filter_class = GoodsFilter

# 写法4  搜索功能  Search查询是模糊查询最佳的效果,在写法3的基础上又加了一些逻辑
# class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     # 设置分页的配置
#     pagination_class = GoodsPagination
#     filter_backends = (DjangoFilterBackend,filters.SearchFilter)
#     filter_class = GoodsFilter
#     search_fields = ('^name','=goods_brief')  # 也可以嵌套加入正则表达式的语法

# drf 的排序 ----------------------------------------------------------------------------------------------------
class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    1.使用drf框架7行完成：商品列表页展示，分页，过滤，搜索，排序（前端呈现web可视化API界面）
    2.后端人员不需要写太多文档表明接口对应的参数，直接通过页面中的过滤器测试得到API地址
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 设置分页的配置
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication,)  # 商品是公开列表页，不能配置token的验证
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name','goods_brief','goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

# 项目实战环节 =========================================================================
class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer







