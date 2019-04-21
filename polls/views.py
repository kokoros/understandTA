from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from polls.models import Pets, Collect, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from django.views.decorators.csrf import csrf_exempt

# uname = 'test'


# 初始化默认显示前100条
def pets(request):
    pet = Pets.objects.all()[:100]
    page = request.GET.get('page')
    pagin = Paginator(pet, 8)
    try:
        posts = pagin.page(page)
    except PageNotAnInteger:
        posts = pagin.page(1)
    except EmptyPage:
        posts = pagin.page(pagin.num_pages)
    data = {'posts': posts}
    return render(request, 'polls/pet.html', context=data)

#商品添加到购物车
def goodadd(request):
    #判断用户是否登录
    if not request.session.get('is_login', None):
        return redirect("/login")
    request.encoding = 'utf-8'
    if 'collect' in request.GET:  # 判断是否有添加到购物车请求
        pid = request.GET['collect']
        collectone = Collect.objects.filter(pid=pid, cenable=0)
        getpetone = Pets.objects.filter(id=pid)
        cprice = getpetone[0].pprice
        if collectone.count() < 1:  # 如果该购车车没有该商品就添加
            # 1.插入数据

            cuser = request.session['user_name']  # 此处替换保留的用户名　
            cname = getpetone[0].pname
            ctype = getpetone[0].ptype
            cpath = getpetone[0].ppath
            cdes = getpetone[0].pdescribe
            ctime = time.strftime("%Y-%m-%d %X")  # 加入购物车时间　
            # cnumber为商品数量
            col = Collect(pid=pid, uname=cuser, cname=cname, ctype=ctype, ctime=ctime, cnumber=1, cdescribe=cdes,
                          cprice=cprice, callprice=cprice, ctypeid=0, cpath=cpath)
            col.save()
        else:  # 购物车数量增加
            cnumold = collectone[0].cnumber
            allprice = collectone[0].callprice
            newallprice = cprice + allprice
            cnumnew = cnumold + 1
            coladdnum = Collect.objects.get(pid=pid, cenable=0)
            coladdnum.cnumber = cnumnew
            coladdnum.callprice = newallprice
            coladdnum.save()
        pnumold = getpetone[0].pnumber
        pnumnew = pnumold + 1
        petnew = Pets.objects.get(id=pid)
        petnew.pnumber = pnumnew
        petnew.save()
    pet = Pets.objects.all()[:100]
    page = request.GET.get('page')
    pagin = Paginator(pet, 8)
    try:
        posts = pagin.page(page)
    except PageNotAnInteger:
        posts = pagin.page(1)
    except EmptyPage:
        posts = pagin.page(pagin.num_pages)
    data = {'posts': posts}
    return render(request, 'polls/pet.html', context=data)


# 根据名称模糊查询
def showbyname(request):
    request.encoding = 'utf-8'
    if 'query' in request.GET:
        pname = request.GET['query']
        # 根据名称模糊获取
        print('shwobyname:', pname)
        pet = Pets.objects.filter(pname__contains='%s' % pname)
        page = request.GET.get('page')
        pagin = Paginator(pet, 8)
        try:
            posts = pagin.page(page)
        except PageNotAnInteger:
            posts = pagin.page(1)
        except EmptyPage:
            posts = pagin.page(pagin.num_pages)
        data = {'posts': posts}
        return render(request, 'polls/pet.html', context=data)


# 购物车模糊查询
def goodbyname(request):
    request.encoding = 'utf-8'
    uname = request.session['user_name']
    if 'good' in request.GET:
        cname = request.GET['good']
        posts = Collect.objects.filter(cname__contains=cname, uname=uname, cenable=0)
        data = {'posts': posts}
        return render(request, 'polls/collect.html', context=data)


# 购物车默认加载，增加或者减少数据，动态生成价格
def collect(request):
    if not request.session.get('is_login', None):
        return redirect("/login")
    request.encoding = 'utf-8'
    #用户名
    username = request.session['user_name']
    posts = Collect.objects.all().filter(uname=username, cenable=0)[:6]
    print('ind')
    return render(request, 'polls/collect.html', {'posts': posts})


# 购物车到订单
def getgood(request):
    jid = request.GET['jid']
    print('jid:', jid)
    posts = Collect.objects.filter(id=jid)
    data = {'posts': posts}
    return render(request, 'polls/order.html', context=data)


# 显示订单数据
def orderlist(request):
    username = request.session['user_name']
    posts=Order.objects.filter(uname=username,oenable=0)
    data={'posts':posts}
    return render(request,'polls/orderlist.html',context=data)

# 提交订单方案１取消 ostatue:-1表示已经删除的订单；0表示提交未支付；１表示已经支付待发货；２已发货未收货；３确认收货交易完成｜｜oenable:0为有效数据，－１为无效数据
# 使用备用字段显示订单状态：odesc
def orderput(request):
    uname = request.session['user_name']  # 用户名
    request.encoding = 'utf-8'
    if 'address' in request.GET and 'phone' in request.GET and 'uname' in request.GET:
        add = request.GET['address']
        pho = request.GET['phone']
        ouser = request.GET['uname']
        desc = request.GET['desc']
        ocid = request.GET['oid']

        # 根据collect_id获取信息
        start=ocid.index('=')
        ocid=ocid[start+1:]
        print('ocid:',ocid,pho)
        col=Collect.objects.filter(id=ocid)
        print('col',col)
        oname=col[0].cname
        oprice=col[0].callprice
        onum=col[0].cnumber
        opath=col[0].cpath
        otime=time.strftime("%Y-%m-%d %X")         
        
        adord = Order(cid=ocid, uname=uname, oname=oname, oprice=oprice, onum=onum, oaddress=add, ouser=ouser,
                      ophone=pho, otime=otime, oenable=0, ostatue=0, opath=opath, odesc='未支付')
        adord.save()
        coll = Collect.objects.get(id=ocid)
        coll.cenable = -2  # 购物车到订单状态调整
        coll.save()
    posts = Order.objects.all().filter(uname=uname, oenable=0)[:6]
    data = {'posts': posts}
    return render(request, 'polls/orderlist.html', context=data)


# 查询订单
def orderquery(request):
    request.encoding = 'utf-8'
    uname = request.session['user_name']
    if 'ordername' in request.GET:
        cname = request.GET['ordername']
        posts = Order.objects.filter(oname__contains=cname, uname=uname, oenable=0)
        data = {'posts': posts}
        return render(request, 'polls/orderlist.html', context=data)


# 删除订单
def orderdelete(request):
    if 'odid' in request.GET:  # 更新状态不做删除
        did = request.GET['odid']
        ordd = Order.objects.get(id=did)
        ordd.oenable = -1
        ordd.ostatue = -1
        ordd.save()
    uname = request.session['user_name']
    posts = Order.objects.all().filter(uname=uname, oenable=0)[:6]
    data = {'posts': posts}
    return render(request, 'polls/orderlist.html', context=data)


# 支付跳转
def orderpay(request):
    return render(request, 'polls/pay.html')


# 支付结果 密码为：666666
@csrf_exempt
def payresult(request):
    pawss = '666666'
    if request.POST:
        paw = request.POST['paw']
        # print(paw)
        olid = request.POST['olid']
        start = olid.index('=')
        olid = olid[start + 1:]
        print(olid)
        orde = Order.objects.get(id=olid)
        uname = request.session['user_name']
        if paw == pawss:
            print('正确')
            orde.odesc = '待发货'
            orde.save()
            posts = Order.objects.filter(uname=uname, oenable=0)
            data = {'posts': posts}
            return render(request, 'polls/orderlist.html', context=data)
        else:
            orde.odesc = '待支付'
            orde.save()
            posts = Order.objects.filter(uname=uname, oenable=0)
            data = {'posts': posts}
            return render(request, 'polls/orderlist.html', context=data)


# 显示商品详情
def petdetail(request):
    petid=request.GET['detailid']
    posts=Pets.objects.filter(id=petid)
    print(posts)
    data={'posts':posts}
    return render(request,'polls/petdetail.html',context=data)
# 商品详情直接下单 不经过购物车，数量无法调整,需要是登录状态
def deorders(request):
    #判断用户是否登录
    if not request.session.get('is_login', None):
        return redirect("/login")
        
    jid=request.GET['jid']
    print('jid:',jid)
    posts=Pets.objects.filter(id=jid)
    data={'posts':posts}
    return render(request,'polls/orderde.html',context=data)
    
# 从详情直接确认订单，需要登录状态
def orderputde(request):
    #判断用户是否登录
    if not request.session.get('is_login', None):
        return redirect("/login")
        
    uname=request.session['user_name']  #用户名
    request.encoding='utf-8'
    if 'address' in request.GET and 'phone' in request.GET and  'uname' in request.GET:
        add=request.GET['address'] 
        pho=request.GET['phone']
        ouser=request.GET['uname']
        desc=request.GET['desc']
        ocid=request.GET['oid']
       
        #根据collect_id获取信息
        start=ocid.index('=')
        ocid=ocid[start+1:]
        print('ocid:',ocid,pho)
        col=Pets.objects.filter(id=ocid)
        print('col',col)
        oname=col[0].pname
        oprice=col[0].pprice
        onum=1
        opath=col[0].ppath
        otime=time.strftime("%Y-%m-%d %X")
        adord=Order(cid=ocid,uname=uname,oname=oname,oprice=oprice,onum=onum,oaddress=add,ouser=ouser,ophone=pho,otime=otime,oenable=0,ostatue=1,opath=opath,odesc='未支付')
        adord.save()    
    posts=Order.objects.all().filter(uname=uname,oenable=0)[:6]
    data={'posts':posts}
    return  render(request,'polls/orderlist.html',context=data)
# 商品详情到购物车
def degoodadd(request):
    request.encoding='utf-8'
    #判断用户是否登录
    if not request.session.get('is_login', None):
        return redirect("/login")
    if 'collect' in  request.GET:#判断是否有添加到购物车请求
        pid=request.GET['collect']
        collectone=Collect.objects.filter(pid=pid,cenable=0)  #
        print('collect',collectone)
        getpetone=Pets.objects.filter(id=pid)
        cprice=getpetone[0].pprice
        if collectone.count()<1:#如果该购车车没有该商品就添加
            #1.插入数据
            cuser=request.session['user_name']  #此处替换保留的用户名　
            cname=getpetone[0].pname
            ctype=getpetone[0].ptype
            cpath=getpetone[0].ppath
            cdes=getpetone[0].pdescribe
            ctime=time.strftime("%Y-%m-%d %X")  #加入购车车时间　
            #cnumber为商品数量
            col=Collect(pid=pid,uname=cuser,cname=cname,ctype=ctype,ctime=ctime,cnumber=1,cdescribe=cdes,cprice=cprice,callprice=cprice,ctypeid=0,cpath=cpath)
            col.save()
        else: #购物车数量增加
            cnumold=collectone[0].cnumber
            allprice=collectone[0].callprice
            newallprice=cprice+allprice
            cnumnew=cnumold+1
            coladdnum=Collect.objects.get(pid=pid,cenable=0)
            coladdnum.cnumber=cnumnew
            coladdnum.callprice=newallprice
            coladdnum.save()
        pnumold=getpetone[0].pnumber
        pnumnew=pnumold+1
        petnew=Pets.objects.get(id=pid)
        petnew.pnumber=pnumnew
        petnew.save()
    uname = request.session['user_name']
    posts=Collect.objects.all().filter(uname=uname,cenable=0)[:6]
    data={'posts':posts}
    return render(request,'polls/collect.html',context=data)    
       
def colles(request):
    request.encoding='utf-8'
    #判断用户是否登录
    if not request.session.get('is_login', None):
        return redirect("/login")
        
    if 'sid' in request.GET: #减少数量
        sid=request.GET['sid']
        print('sid')
        coll=Collect.objects.filter(id=sid)
        oldnum=coll[0].cnumber
        price=coll[0].cprice 
        oldallprice=coll[0].callprice
        print('oldnum:',oldnum)   
        if oldnum>1: #数量改变同时金额也发生变化
            newnum=oldnum-1
            allprice=oldallprice-price
            snum=Collect.objects.get(id=sid)
            snum.callprice=allprice
            snum.cnumber=newnum
            snum.save()
    username=request.session['user_name'] 
    posts=Collect.objects.all().filter(uname=username,cenable=0)[:6]
    print('ind')
    return render(request,'polls/collect.html',{'posts':posts})

def coladd(request):
    request.encoding='utf-8'
    #判断用户是否登录
    if not request.session.get('is_login', None):
        return redirect("/login")
            
    if  'aid' in request.GET:
        aid=request.GET['aid']
        print('sid')
        coll=Collect.objects.filter(id=aid)
        oldnum=coll[0].cnumber
        price=coll[0].cprice 
        oldallprice=coll[0].callprice
        print('oldnum:',oldnum)   
        if oldnum<10000:    #假设最大库存１０００　金额发生变化
            newnum=oldnum+1
            allprice=oldallprice+price
            anum=Collect.objects.get(id=aid)
            anum.cnumber=newnum
            anum.callprice=allprice
            anum.save()
    username=request.session['user_name']
    posts=Collect.objects.all().filter(uname=username,cenable=0)[:6]
    print('ind')
    return render(request,'polls/collect.html',{'posts':posts})


def coldel(request):
    request.encoding='utf-8'
    #判断用户是否登录
    if not request.session.get('is_login', None):
        return redirect("/login")
        
    if 'did' in request.GET:
        did=request.GET['did']
        col=Collect.objects.get(id=did)
        col.cenable=-1
        col.save()
    username=request.session['user_name']
    posts=Collect.objects.all().filter(uname=username,cenable=0)[:6]
    print('ind')
    return render(request,'polls/collect.html',{'posts':posts})






