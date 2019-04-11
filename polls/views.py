from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from polls.models import Pets,Collect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import time
# 初始化默认显示前100条
def  pets(request):
    request.encoding='utf-8'
    if 'collect' in  request.GET:#判断是否有收藏请求
        pid=request.GET['collect']
        collectone=Collect.objects.filter(pid=pid)
        if collectone.count()<1:#如果已经收藏直接返回主界面,反之就直接刷新数据
            #1.插入数据
            cuser='test'
            getpetone=Pets.objects.filter(id=pid)
            cname=getpetone[0].pname
            ctype=getpetone[0].ptype
            cpath=getpetone[0].ppath
            ctime=ti=time.strftime("%Y-%m-%d %X")
            #number有效数据的标志:1为有效,0为无效
            col=Collect(pid=pid,uname=cuser,cname=cname,ctype=ctype,ctime=ctime,cnumber=1)
            col.save()
            #更新增加收藏量
            pnumold=getpetone[0].pnumber
            pnumnew=pnumold+1
            petnew=Pets.objects.get(id=pid)
            petnew.pnumber=pnumnew
            petnew.save()
    pet=Pets.objects.all()[:100]
    page=request.GET.get('page')
    pagin=Paginator(pet,8)
    try:
        posts=pagin.page(page)
    except PageNotAnInteger:
        posts=pagin.page(1)
    except EmptyPage:
        posts=pagin.page(pagin.num_pages)
    data={'posts':posts}
    return render(request, 'polls/pet.html', context=data)
# 根据名称模糊查询
def showbyname(request):
    request.encoding='utf-8'
    if 'query' in request.GET:
        pname=request.GET['query']
        # 根据名称模糊获取
        print('shwobyname:',pname)
        pet=Pets.objects.filter(pname__contains='%s'%pname)
        page=request.GET.get('page')
        pagin=Paginator(pet,8)
        try:
            posts=pagin.page(page)
        except PageNotAnInteger:
            posts=pagin.page(1)
        except EmptyPage:
            posts=pagin.page(pagin.num_pages)
        data={'posts':posts}
        return render(request, 'polls/pet.html', context=data)
#图片识别调整和上传

def  petphoto(request):
    file_obj=request.FILES.get('file',None)
    print('filename:',file_obj)
    return render(request,'petadd.html')



