from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from random import choice
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler

from .serializers import SmsSerializer,UserRegSerializer
from utils.yunpian import YunPian
from MxShop.settings import APIKEY
from .models import VerifyCode

# Create your views here.

# get_user_model方法会去setting中找AUTH_USER_MODEL
User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            #用户名和手机都能登录
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    '''
    发送短信验证码
    '''
    serializer_class = SmsSerializer

    # 生成短信验证码(四位数字)
    def generate_code(self):
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 设置为True，直接抛异常

        # 取出serializer中的传递进来的参数,进行验证码的发送
        mobile = serializer.validated_data['mobile']
        yunpian = YunPian(APIKEY)

        # 生成四位数字验证码
        code = self.generate_code()

        # 根据API返回的状态值，判断成功与否
        sms_status = yunpian.send_sms(code=code,mobile=mobile)
        if sms_status['code'] != 0:
            return Response({
                'mobile':sms_status['msg']
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            # 短信发送成功后，保存验证码到数据库
            code_record = VerifyCode(code=code,mobile=mobile)
            code_record.save()
            return Response({
                'mobile':mobile
            },status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin,viewsets.GenericViewSet):
    '''
    用户
    '''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    # 返回给用户tokenz值，实现自动登陆
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # 生成JWT形式的Token
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 返回user对象
    def perform_create(self, serializer):
        return serializer.save()




















