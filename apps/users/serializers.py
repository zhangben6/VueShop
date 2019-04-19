# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/15 22:01'

import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import VerifyCode
from MxShop.settings import REGEX_MOBILE
from datetime import datetime, timedelta
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
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')

        # Re验证手机号码是否合法
        # if re.match(REGEX_MOBILE,mobile):
        #     raise serializers.ValidationError('手机号码非法')

        # 验证发送频率的限制
        two_min_ago = datetime.now() - timedelta(hours=0, minutes=2, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=two_min_ago, mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送请求未超过60s')

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True,
                                 label='验证码',
                                 write_only=True,
                                 max_length=4,
                                 min_length=4,
                                 help_text='验证码',
                                 error_messages={
                                     'required': '请输入验证码',
                                     'blank': '请输入验证码',
                                     'max_length': '验证码格式错误1',
                                     'min_length': '验证码格式错误2',
                                  })

    # 验证username
    username = serializers.CharField(label='用户名',required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在1')])

    # 密码的配置
    password = serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        label='密码'
    )


    # def create(self, validated_data):
    #     # 继承父类的方法，返回值可以获得user对象
    #     user = super(UserRegSerializer,self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    # 验证码的验证操作
    def validate_code(self, code):
        # 验证数据库中是否存在此验证码：先按照时间顺序排序
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            # 取出最后一条验证码
            last_records = verify_records[0]

            # 计算出五分钟前的时间
            five_min_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)

            if five_min_ago > last_records.add_time:
                raise serializers.ValidationError('验证码过期')

            if last_records.code != code:
                raise serializers.ValidationError('验证码错误')

            # 验证没问题返回正确的code值
            return code

        # 不存在记录的情况
        else:
            raise serializers.ValidationError('验证码不存在1')

    # 此函数功能不仅仅作用于一个字段，而是作用于全局的serializer，attrs参数特殊意义
    def validate(self, attrs):
        '''全局的serializer一些处理'''
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile','password')


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户详情序列化类
    '''
    class Meta:
        model = User
        fields = ('birthday','mobile','gender','email','name')