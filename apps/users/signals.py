# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/17 15:55'

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# get_user_model方法会去setting中找AUTH_USER_MODEL
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
