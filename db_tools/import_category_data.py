# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/12 11:14'

# 独立使用django的model

import sys
import os

# 得到目前这个脚本文件的目录
pwd = os.path.dirname(os.path.realpath(__file__))

# 将整个项目的根目录加入到python根搜索路径之下
sys.path.append(pwd+'../')

# 如果要单独使用django model  首先设置环境变量跟manage.py文件保持一致
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")

import django
django.setup()

# ↑  以上的步骤用来初始化环境

from goods.models import GoodsCategory
from db_tools.data.category_data import row_data

for lev1_cat in row_data:
    lev1_instance = GoodsCategory()
    lev1_instance.code = lev1_cat['code']
    lev1_instance.name = lev1_cat['name']
    lev1_instance.category_type = 1
    lev1_instance.save()

    for lev2_cat in lev1_cat['sub_categorys']:
        lev2_instance = GoodsCategory()
        lev2_instance.code = lev2_cat['code']
        lev2_instance.name = lev2_cat['name']
        lev2_instance.category_type = 2
        # 第二类别添加父类
        lev2_instance.parent_category = lev1_instance
        lev2_instance.save()

        for lev3_cat in lev2_cat['sub_categorys']:
            lev3_instance = GoodsCategory()
            lev3_instance.code = lev3_cat['code']
            lev3_instance.name = lev3_cat['name']
            lev3_instance.category_type = 3
            # 第二类别添加父类
            lev3_instance.parent_category = lev2_instance
            lev3_instance.save()
