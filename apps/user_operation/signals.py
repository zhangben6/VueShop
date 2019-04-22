# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/22 14:59'

from django.conf import settings
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from user_operation.models import UserFav


# 用户收藏的时候，django会发送一个post_save的信号量
@receiver(post_save, sender=UserFav)
def create_userFav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

@receiver(post_delete, sender=UserFav)
def delete_userFav(sender, instance=None, created=False, **kwargs):
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()
