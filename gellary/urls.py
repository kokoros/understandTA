from django.urls import path
from django.conf.urls import include,url
from . import views

urlpatterns = [
    # path('',views.index,name='index'),
    # path('',views.getinfos,name='getinfos'),
    url(r'^index/',views.index),
    url(r'^getinfos/',views.getinfos),
    url(r'^queryliuyans/',views.queryliuyans),
    url(r'^changjiangyihao/',views.changjiangyihao),
    url(r'^changjiangerhao/',views.changjiangerhao),
    url(r'^changjiangsanhao/',views.changjiangsanhao),
    url(r'^changjiangsihao/',views.changjiangsihao),
    url(r'^changjiangwuhao/',views.changjiangwuhao),
    url(r'^changjiangliuhao/',views.changjiangliuhao),
    url(r'^changjiangqihao/',views.changjiangqihao),
    url(r'^changjiangbahao/',views.changjiangbahao),
    url(r'^liuyans/',views.liuyans),
]