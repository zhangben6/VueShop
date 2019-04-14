# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/13 10:22'

from rest_framework import generics
from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Goods

class GoodsFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    # name = filters.CharFilter(field_name='name',lookup_expr='icontains')
    top_category = filters.NumberFilter(field_name='查询某一类别商品',method='top_category_filter')

    def top_category_filter(self,queryset,name,value):
        queryset = queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))
        return queryset
    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']
