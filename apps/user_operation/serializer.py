# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/18 21:57'

from rest_framework import serializers

from .models import UserFav

class UserFavSerializer(serializers.ModelSerializer):
    # 获取到当前的用户

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserFav
        fields = ('user','goods','id')

