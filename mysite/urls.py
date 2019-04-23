"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views 
from django.conf.urls import include, url

#为用户上传的文件提供服务
from django.conf.urls.static import static
from django.conf import settings

#导入polls文件夹中的views,重命名为polls_views
from polls import views as polls_views

#导入公告views
from bulletin import views as bulletin_views



urlpatterns = [
    #后台
    path('admin/', admin.site.urls),
    #主页
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    #生成验证码
    path('captcha', include('captcha.urls')),

    #修改密码
    path('change_password/',views.change_password),
    #确认邮件确认请求
    path('confirm/',views.user_confirm),
    #申请重置密码的界面
    path('reset_password/',views.reset_password),
    #真正重置密码的界面
    path('reset_password_ready/',views.reset_password_ready),
    #展示个人信息
    path('information/', views.information),
    #修改个人信息
    path('modify/', views.modify),
    # 首页 /
    path('', views.home),
    #关于我们
    path('aboutus/', views.aboutus),

    # 裁剪并上传头像
    path('head_photo/', views.head_photo),
    #处理裁剪提交
    path('handing_head/', views.handing_head),

    #重新发送邮件
    path('send_again_register/', views.send_again_register),

    #Ajax验证验证码
    path('ajax_captcha/', views.ajax_captcha),

    #验证邮箱在不在数据库
    path('ajax_user_email_isalive/', views.ajax_user_email_isalive),
    #验证用户名在不在数据库
    path('ajax_user_name_isalive/', views.ajax_user_name_isalive),

    #导入polls中的路由
    path(r'pet', polls_views.pets),
    path(r'query', polls_views.showbyname),
    path(r'collect', polls_views.collect),
    path(r'good', polls_views.goodbyname),
    path(r'orders', polls_views.getgood),
    path(r'showorder', polls_views.orderlist),
    path(r'orderput', polls_views.orderput),
    path(r'goodadd', polls_views.goodadd),
    path(r'orderquery', polls_views.orderquery),
    path(r'delorder', polls_views.orderdelete),
    path(r'pay', polls_views.orderpay),
    path(r'orderpay', polls_views.payresult),
    path(r'petdetail', polls_views.petdetail),
    path(r'deorders', polls_views.deorders),
    path(r'degoodadd', polls_views.degoodadd),
    path(r'delorderput', polls_views.orderputde),
    path(r'colles', polls_views.colles),
    path(r'coladd', polls_views.coladd),
    path(r'coldel', polls_views.coldel),
    path(r'oresult', polls_views.oresult),

    #导入公告
    path('01-Find_pet/', bulletin_views.views),
    path('02-adopter/', bulletin_views.adopt),
    path('02-server/', bulletin_views.server02),
    path('03-server/', bulletin_views.server03),
    path('03-publish_notices/', bulletin_views.publish),

    #导入明星宠物墙
    path('gellary/', include('gellary.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
