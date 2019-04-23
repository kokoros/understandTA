from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader, Context, Template, RequestContext
from gellary.models import *
from .forms import *
from django.template import RequestContext


def index(request):
    user_list = User.objects.all()
    if request.method == 'GET':
        return render(request, "gellary/index.html")
    else:
        pname = request.POST.get('pname')
        print('pname', pname)
        pwords = request.POST.get('pwords', None)
        try:
            user = User.objects.get(pname=pname)
            data = {'user': user}
            if user:
                return render(request, 'gellary/getinfos.html', context=data)
        except Exception as e:
            print('查询失败:', e)
            return HttpResponse("查询失败")


def liuyans(request):
    new_user = Bbs()
    user_list = Bbs.objects.all()
    if request.method == 'GET':
        return render(request, 'gellary/liuyans.html')
    else:
        new_user = Bbs.objects.create()
        new_user.uname = request.POST.get('uname', None)
        new_user.ubbs = request.POST.get('ubbs', None)
        data = {'new_user': new_user}
        new_user.save()
        return render(request, 'gellary/index.html', locals())


def queryliuyans(request):
    user_list = User.objects.all()
    if request.method == 'GET':
        return render(request, "gellary/queryliuyans.html")
    else:
        user = request.POST.get("uname", None)
        uname = Bbs.objects.filter(uname=user)
        return render(request, 'gellary/queryliuyans.html', {'uname': uname, 'user': user})


def getinfos(request):
    return render(request, 'gellary/getinfos.html')


def changjiangyihao(request):
    pname = User.objects.get(pname="小米")
    return render(request, 'gellary/changjiangyihao.html', {'pname': pname})


def changjiangerhao(request):
    pname = User.objects.get(pname="木木")
    return render(request, 'gellary/changjiangerhao.html', {'pname': pname})


def changjiangsanhao(request):
    pname = User.objects.get(pname="妙妙")
    return render(request, 'gellary/changjiangsanhao.html', {'pname': pname})


def changjiangsihao(request):
    pname = User.objects.get(pname="小黑")
    return render(request, 'gellary/changjiangsihao.html', {'pname': pname})


def changjiangwuhao(request):
    pname = User.objects.get(pname="小黄")
    return render(request, 'gellary/changjiangwuhao.html', {'pname': pname})


def changjiangliuhao(request):
    pname = User.objects.get(pname="艾克")
    return render(request, 'gellary/changjiangliuhao.html', {'pname': pname})


def changjiangqihao(request):
    pname = User.objects.get(pname="汤姆")
    return render(request, 'gellary/changjiangqihao.html', {'pname': pname})


def changjiangbahao(request):
    pname = User.objects.get(pname="杰瑞")
    return render(request, 'gellary/changjiangbahao.html', {'pname': pname})