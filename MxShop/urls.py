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
from django.views.generic import TemplateView

from goods.views import GoodsListViewSet,CategoryViewSet,HotSearchViewSet,BannerViewSet
from users.views import SmsCodeViewSet,UserViewSet
from MxShop.settings import MEDIA_ROOT
from user_operation.views import UserFavViewset,LeavingMessageViewset,AddressViewSet
from trade.views import shoppingCartViewset,OrderViewSet,AlipayView
from goods.views import IndexCategoryViewSet


router = DefaultRouter()

# 配置goods的url
router.register(r'goods',GoodsListViewSet,base_name='goods')

# 配置category的url
router.register(r'categorys',CategoryViewSet,base_name='categorys')

# 发送验证码的接口
router.register(r'codes',SmsCodeViewSet,base_name='codes')

# 用户注册页面
router.register(r'users',UserViewSet,base_name='users')

# 用户收藏api
router.register(r'userfavs',UserFavViewset,base_name='userfavs')

# 留言功能
router.register(r'messages',LeavingMessageViewset,base_name='messages')

# 收货地址
router.register(r'address',AddressViewSet,base_name='address')

# 购物车相关API
router.register(r'shopcarts',shoppingCartViewset,base_name='shopcarts')

# 创建订单的接口
router.register(r'orders',OrderViewSet,base_name='orders')

# 热搜词的接口
router.register(r'hotsearchs',HotSearchViewSet,base_name='hotsearchs')

# 首页轮播图的接口
router.register(r'banners',BannerViewSet,base_name='banners')

# 首页商品系列数据接口
router.register(r'indexgoods',IndexCategoryViewSet,base_name='indexgoods')



# goods_list = GoodsListViewSet.as_view({
#     'get':'list',
#  })


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),

    # Vue前端项目生成的静态文件和html访问路径
    url(r'^index/',TemplateView.as_view(template_name='index.html'),name='index'),

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

    # 处理支付宝支付的同步异步支付结果
    url(r'^alipay/return/',AlipayView.as_view(),name='alipay')

]
