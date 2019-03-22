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
from django.conf.urls import include


urlpatterns = [
    #后台
    path('admin/', admin.site.urls),
    #主页
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('captcha',include('captcha.urls')),
    #修改密码
    path('change_password/',views.change_password),
    #确认邮件确认请求
    path('confirm/',views.user_confirm),
    
    #申请重置密码的界面
    path('reset_password/',views.reset_password),
    
    #真正重置密码的界面
    path('reset_password_ready/',views.reset_password_ready),
    
]
