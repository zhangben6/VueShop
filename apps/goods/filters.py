# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/13 10:22'

from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Goods

class GoodsFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')
    class Meta:
        model = Goods
        fields = ['min_price', 'max_price','name']
