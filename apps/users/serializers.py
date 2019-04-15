# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/15 22:01'

import re
from rest_framework import serializers
from .models import VerifyCode
from MxShop.settings import REGEX_MOBILE
from datetime import datetime,timedelta
# get_user_model方法会去setting中找AUTH_USER_MODEL
from django.contrib.auth import get_user_model
User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param data:
        :return:
        '''

        # 手机号码是否注册
        if User.object.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')

        # Re验证手机号码是否合法
        if re.match(REGEX_MOBILE,mobile):
            raise  serializers.ValidationError('手机号码非法')

        # 验证发送频率的限制
        two_min_ago = datetime.now() - timedelta(hours=0,minutes=2,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=two_min_ago,mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送请求未超过60s')

        return mobile

