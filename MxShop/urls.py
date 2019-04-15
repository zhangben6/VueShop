"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
import xadmin
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet,CategoryViewSet
from MxShop.settings import MEDIA_ROOT

router = DefaultRouter()


# 配置goods的url
router.register(r'goods',GoodsListViewSet,base_name='goods')

# 配置category的url
router.register(r'categorys',CategoryViewSet,base_name='categorys')


# goods_list = GoodsListViewSet.as_view({
#     'get':'list',
#  })


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),

    # 富文本编辑
    url(r'ueditor/',include('DjangoUeditor.urls')),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 商品列表页面api
    # url(r'^goods/$',goods_list,name='goods-list'),

    # drf框架的文档功能
    url(r'docs/',include_docs_urls(title='Rapzhang线上超市')),# 地址一定不要加上$

    # 使用router url的配置
    url(r'^', include(router.urls)),

    # drf自带的token认证模式，创建数据库token表，进行查询认证
    url(r'^api-token-auth/', views.obtain_auth_token),

    # drf中JWT的认证接口
    url(r'^login/', obtain_jwt_token),

]
