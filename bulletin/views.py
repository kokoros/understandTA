from django.shortcuts import render, redirect, HttpResponse
#导入本app数据表
from bulletin import models
#导入日期时间
from datetime import datetime
#导入系统
import os

# Create your views here.

def views(request):
    #只显示前三个
    find_pet = models.Find_pet.objects.all()[:3]
    return render(request, 'bulletin/01-Find_pet.html', locals())

def adopt(request):
    return render(request, 'bulletin/02-adopter.html')

def server02(request):
    #判断是否登录
    if not request.session.get('is_login', None):
        return redirect("/login")
    #如果是get请求
    if request.method == 'GET':
        return render(request, 'bulletin/02-adopter.html')
    else:
        f = request.FILES['pic']
        # 拼出的绝对路径
        # 得到最外层mysite的绝对路径 /home/..../mysite
        basedir = os.path.dirname(os.path.dirname(__file__))
        # 默认公告图片储存的绝对路径
        default_path = os.path.join(basedir, 'static/bulletin/images', f.name)
        print('公告图片绝对路径', default_path)
        try:
            #储存图片
            #新建图片文件
            with open(default_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        except Exception as e:
            print('保存公告上传图片失败', e)
        finally:
            f.close()
            destination.close()


        adopter = models.Adopter()
        adopter.username = request.session['user_name']
        adopter.title = request.POST['title']
        adopter.main = request.POST['main']
        adopter.time = datetime.utcnow()
        adopter.area = request.POST['area']
        adopter.pet_type = request.POST['type']
        adopter.pic = 'bulletin/images/' + f.name
        #保存到数据库
        adopter.save()
        return HttpResponse("提交成功")

def publish(request):
    return render(request, 'bulletin/03-publish_notices.html')

def server03(request):
    #判断是否登录
    if not request.session.get('is_login', None):
        return redirect("/login")
    if request.method == 'GET':
        return render(request, 'bulletin/02-adopter.html')
    else:
        f = request.FILES['pic']

        # 拼出的绝对路径
        # 得到最外层mysite的绝对路径 /home/..../mysite
        basedir = os.path.dirname(os.path.dirname(__file__))
        # 默认公告图片储存的绝对路径
        default_path = os.path.join(basedir, 'static/bulletin/images', f.name)
        print('公告图片绝对路径', default_path)
        try:
            #储存图片
            #新建图片文件
            with open(default_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        except Exception as e:
            print('保存公告上传图片失败', e)
        finally:
            f.close()
            destination.close()

        find_pet = models.Find_pet()
        # 用户名
        username = request.session['user_name']

        find_pet.username = username
        find_pet.title= request.POST['title']
        find_pet.main= request.POST['main']
        find_pet.time=datetime.utcnow()
        find_pet.area= request.POST['area']
        find_pet.thanks= request.POST['thanks']
        find_pet.pic= 'bulletin/images/'+f.name
        #保存
        find_pet.save()
        return HttpResponse("提交成功")