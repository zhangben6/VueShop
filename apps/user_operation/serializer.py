# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/18 21:57'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav,UserAddress
from goods.serializers import GoodsSerializer
from .models import UserLeavingMessage


class UserFavDetailSerializer(serializers.ModelSerializer):
    '''
    用户收藏详情
    '''
    #通过商品id获取收藏的商品，需要嵌套商品的序列化
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):

    # 获取到当前的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        # validate实现唯一联合，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                # message的信息可以自定义
                message="已经收藏"
            )
        ]

        fields = ('user','goods','id')

class LeavingMessageSerializer(serializers.ModelSerializer):
    # 获取到当前的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # 设置了read_only之后，字段的值只返回不提交
    add_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M')
    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject','message','file','id','add_time')


class AddressSerializer(serializers.ModelSerializer):
    # 获取到当前的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 设置了read_only之后，字段的值只返回不提交
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = UserAddress
        fields = ('id','user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile','add_time')
