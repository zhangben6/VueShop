# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/12 16:24'

# 此文件用来实力不用djangorestframework 框架的弊端


import json
from django.views.generic.base import View
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.core import serializers

from goods.models import Goods

class GoodsListView(View):
    def get(self,request):  # 默认传递一个reqeust参数进来
        json_list = []
        goods = Goods.objects.all()[:10]

        # for good in goods:
        #     json_dic = {}
        #     json_dic['name'] = good.name
        #     json_dic['category'] = good.category.name
        #     json_dic['market_price'] = good.market_price
        #     json_list.append(json_dic)

        # for good in goods:
        #     json_dic = model_to_dict(good)
        #     json_list.append(json_dic)
        # return HttpResponse(json.dumps(json_list),content_type='application/json')

        # 首先对数据进行序列化操作（转换为字典形式)
        json_data = serializers.serialize('json',goods)

        # 将序列化好的数据全部转换为字符串
        # json_data = json.loads(json_data)

        # 最后再转换成json数据
        return HttpResponse(json_data,content_type='application/json')

