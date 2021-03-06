#coding:utf-8

from django.shortcuts import render, redirect ,HttpResponse
from login import models
from login import forms
import hashlib
import datetime
from django.conf import settings

import os
#导入验证码模块
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
#导入Q查询
from django.db.models import Q
#导入json解决cookies无法存入中文的问题
import json
#导入json响应 方便裁剪图片
from django.http import JsonResponse

#导入取消验证来解决ajax总被拒绝的问题
from django.views.decorators.csrf import csrf_exempt

#导入裁剪图片
from PIL import Image

#随机生成头像名称
import uuid


# Create your views here.

#做一个判断有没有cookies的函数
def judeg_cookies(request):
    if 'username' in request.COOKIES and 'password' in request.COOKIES:
        #获取cookies
        username = request.COOKIES.get('username', None)
        print('未解码前:', username)
        username = json.loads(username)
        print('解码后:', username)
        password = request.COOKIES.get('password', None)
        print('username', username)
        print(password)
        try:
            # 判断是否是数据库中的用户
            user = models.User.objects.get(name=username)
        except Exception as e:
            print('获取用户对象失败:',e)
        #如果密码是对的
        if password == user.password:
            print('密码正确')
            # 设置session
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            #session中添加请求源 如果直接是通过输入网址后点击跳转的,则返回首页
            # print(request.META.get('HTTP_REFERER', '/'))
            request.session['url'] = request.META.get('HTTP_REFERER', '/')

            return redirect("/")
        #删除错误的cookies并重定向到登录界面
        else:
            obj_cookies = redirect('/login')
            # 删除用户和哈希值密码的cookies
            obj_cookies.delete_cookie('username')
            obj_cookies.delete_cookie('password')
            return obj_cookies
    #如果没有cookies
    else:
        pass




#登录
def login(request):
    #判断有没有cookies
    judeg_cookies(request)
    if request.session.get('is_login', None):
        return redirect("/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "所有字段都必须填写正确哦~"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                # 判断是否是邮箱或者用户名
                user = models.User.objects.get(Q(name=username) | Q(email=username))
                #判断是否通过邮件确认
                if not user.has_confirmed:
                    message = "您还未通过邮件确认注册"
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)
                    return render(request, 'login/login.html', locals())
                #哈希值和数据库值对比
                if user.password == hash_code(password):
                    #设置session
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    #读取session
                    url = request.session['url']
                    #如果勾选了记住密码
                    if request.POST.get('chocookies', None):
                        #传递cookies
                        try:
                            obj_cookies = redirect(url, locals())
                            #保存用户和哈希值密码3天
                            #保存为json
                            save_username = json.dumps(user.name)

                            obj_cookies.set_cookie('username', save_username, max_age=3*24*60*60)
                            obj_cookies.set_cookie('password', user.password, max_age=3*24*60*60)

                            return obj_cookies
                        except Exception as e:
                            print('保存cookies失败:', e)
                    #如果不存cookies
                    else:
                        #跳转到get进入登录页面前的一个页面
                        return redirect(url)
                else:
                    message = "密码不正确哦"
            except:
                message = "用户名或邮箱不存在~"
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, "login/login.html", locals())
    #如果是get请求
    else:
        #如果是判断邮箱验证的网址跳转的,就不记录了,跳到首页
        if 'confirm' in request.META.get('HTTP_REFERER', '/'):
            request.session['url'] = '/'
        else:
            #无论登录成功与否,都保存请求源进session
            request.session['url'] = request.META.get('HTTP_REFERER', '/')

        login_form = forms.UserForm()
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'login/login.html', locals())


#用于判断验证码是否正确 captchaStr为用户输入的字符串 captchaHashkey为此时的哈希值
def jarge_captcha(captchaStr, captchaHashkey):
    #如果都有
    if captchaStr and captchaHashkey:
        try:
            # 获取 根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            # 如果验证码匹配
            if get_captcha.response == captchaStr.lower():
                return True
        except:
            return False
    else:
        return False

@csrf_exempt
#获取前端传来的用户字符串和验证码哈希值
def ajax_captcha(request):
    #如果是ajax的请求
    if request.is_ajax():
        #获取用户输入的字符串
        captchaStr = request.GET['captcha_1']
        # print('用户输入:', captchaStr)
        #获取当前哈希值
        captchaHashkey = request.GET['captcha_0']
        # print('当前哈希值:', captchaHashkey)
        #判断是否匹配
        if jarge_captcha(captchaStr, captchaHashkey):
            dic = {
                'ajax_captcha':'1'
            }
            # print('正确!')
        else:
            dic = {
                'ajax_captcha':'0'
            }
            # print('错误!')
        #变成json格式传给前端
        return HttpResponse(json.dumps(dic), content_type='application/json')

@csrf_exempt
#用于判断邮箱在不在数据库中
def ajax_user_email_isalive(request):
    #如果是ajax请求
    if request.is_ajax():
        #接受前端get传来的参数
        user_email = request.GET['user_email']

        #在数据库中查询 如果找到了
        same_user = models.User.objects.filter(email=user_email)
        if same_user:
            dic = {
                'ajax_email': '1'
            }
            # print('找到了')
        #如果没找到
        else:
            dic = {
                'ajax_email': '0'
            }
            # print('没找到')
        #变成json格式传给前端
        return HttpResponse(json.dumps(dic), content_type='application/json')

#判断用户名在不在数据库中
def ajax_user_name_isalive(request):
    # 如果是ajax请求
    if request.is_ajax():
        dic = {}
        # 接受前端get传来的参数
        user_name = request.GET['user_name']
        #如果用户名长度大于10或小于2
        if len(user_name) > 15 or len(user_name) < 2:
            dic = {
                'ajax_name_len': '0'
            }

        # 在数据库中查询 如果找到了
        same_user = models.User.objects.filter(name=user_name)
        if same_user:
            #字典里增加一个键
            dic['ajax_name'] = '1'
            # print('找到了')
        # 如果没找到
        else:
            dic['ajax_name'] = '0'
            # print('没找到')
        # 变成json格式传给前端
        return HttpResponse(json.dumps(dic), content_type='application/json')




#注册
def register(request):
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写内容~"

        # 获取数据
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            pet_type = register_form.cleaned_data['pet_type']
            intro = register_form.cleaned_data['intro']

            if password1 != password2:
                message = "两次输入的密码不同"
                hashkey = CaptchaStore.generate_key()
                image_url = captcha_image_url(hashkey)
                return render(request, 'login/register.html', locals())
            elif len(password1) < 6 or len(password1) > 12:
                message = "密码长度在6-12个字符间"
                hashkey = CaptchaStore.generate_key()
                image_url = captcha_image_url(hashkey)
                return render(request, 'login/register.html', locals())
            elif len(username) > 15 or len(username) < 2:
                message = "用户名长度必须在2-15字符间"
                hashkey = CaptchaStore.generate_key()
                image_url = captcha_image_url(hashkey)
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                #如果用户名存在
                if same_name_user:
                    message = "用户名已存在,请重新输入"
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)
                    return render(request,'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                #如果邮箱存在
                if same_email_user:
                    message = "邮箱已被注册,请换一个邮箱注册"
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)
                    return render(request, 'login/register.html', locals())
                try:
                    #一切都ok时
                    new_user = models.User()
                    new_user.name = username
                    #使用加密密码
                    new_user.password = hash_code(password1)
                    new_user.email = email
                    new_user.sex = sex
                    new_user.pet_type = pet_type
                    new_user.intro = intro
                    #先保存除头像外的数据
                    new_user.save()
                except Exception as e:
                    print('保存新用户数据失败:',e)
                else:
                    print('保存除头像外的新用户数据成功!')

                #查询新用户在数据库中id是多少
                new_id = new_user.id

                #保存默认头像 传入新用户id
                save_default_photo(new_id,new_user)

                #认证注册邮箱
                code = make_confirm_string(new_user, 'ConfirmString')
                try:
                    send_email(email, code, 'register')
                except Exception as e:
                    message = "邮件发送失败,请联网或换一个邮箱重新注册"
                    print('注册拦截异常')
                    #删除数据库中才保存的信息
                    models.User.objects.filter(name=username).delete()
                    #返回注册界面
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)

                    return render(request, 'login/register.html', locals())
                message = "请前往注册邮箱,进行邮箱认证~"
                #跳转到等待邮件确认页面
                return render(request, 'login/confirm.html', locals())
        #如果验证不成功
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'login/register.html', locals())

    register_form = forms.RegisterForm()
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    return render(request, 'login/register.html', locals())



#保存默认头像
def save_default_photo(uid,new_user):
    # 组合路径 以用户id新建文件夹 生成默认头像
    new_path = os.path.join('media', str(uid), "avatar", 'default.jpg')
    #数据库里的头像路径
    new_path_mysql = os.path.join(str(uid), "avatar", 'default.jpg')

    #拼出默认头像的绝对路径
    #得到最外层mysite的绝对路径 /home/..../mysite
    basedir = os.path.dirname(os.path.dirname(__file__))
    #默认头像的绝对路径
    default_path = os.path.join(basedir, 'media/photo/default.jpg')

    #去掉用户头像文件名,返回目录avatar
    directory = os.path.dirname(new_path)
    #因为是新用户,所以直接创建用户文件夹
    os.makedirs(directory)

    try:
        #打开默认头像的文件流
        old_photo = open(default_path,"rb")
        #打开新生成的头像
        #拼出新生成的头像的绝对路径
        new_photo_path = os.path.join(basedir, 'media', new_path_mysql)
        new_photo = open(new_photo_path, 'wb+')
        # 1024字节的读取
        while True:
            chunk = old_photo.read(1024)
            if not chunk:
                break
            new_photo.write(chunk)
    except Exception as e:
        print('保存默认头像失败',e)
    finally:
        old_photo.close()
        new_photo.close()
    try:
        #保存到数据库
        new_user.photo = new_path_mysql
        new_user.save()
        print('保存默认头像成功!')
    except Exception as e:
        print('存储默认头像到数据库失败:',e)









#创建确认码对象
def make_confirm_string(user, string):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #now为盐
    code = hash_code(user.name, now)
    #如果是注册认证
    if string == "ConfirmString":
        #生成并保存确认码
        models.ConfirmString.objects.create(code=code, user=user,)
    elif string == "Reset_ConfirmString":
        #生成并保存确认码
        models.Reset_ConfirmString.objects.create(code=code, user=user,)
        
    return code        


#发送邮件
def send_email(email, code, string):
    from django.core.mail import EmailMultiAlternatives
    #如果是注册时发送的邮件
    if string == "register":

        subject = '来自www.understandta.com的注册确认邮件'

        text_content = '''感谢注册www.understandta.com,这里是您宠物的乐园,专注给宠物提供更好的服务!
        如果您看到这条消息,说明您的邮箱不支持html链接功能,请回信与我们联系
        '''

        html_content = '''
        <p>感谢注册<a href="http://{}/confirm/?code={}&type={}" target=blank>www.understandta.com</a>,
        这里是您宠物的乐园,专注给宠物提供更好的服务!</p>
        <p>请点击站点链接完成注册确认!</p>
        <p>此链接有效期为{}天!</p>
        '''.format('127.0.0.1:8000', code, string, settings.CONFIRM_DAYS)

    #如果是重置密码时发送的邮件
    elif string == "reset":

        subject = '来自www.understandta.com的重置密码确认邮件'

        text_content = '''重置密码请求我们已收到.
        如果您看到这条消息,说明您的邮箱不支持html链接功能,请回信与我们联系
        '''
        
        html_content = '''
        <p>重置密码服务已开启<a href="http://{}/confirm/?code={}&type={}" target=blank>www.understandta.com</a>,
        这里是您宠物的乐园,专注给宠物提供更好的服务!</p>
        <p>请点击站点链接完成重置密码确认!</p>
        <p>此链接有效期为{}天!</p>
        '''.format('127.0.0.1:8000', code, string, settings.RESET_DAYS)
    #试图发送邮件
    # try:
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # except Exception as e:
    #     print('邮件发送失败:',e)


def logout(request):
    if not request.session.get('is_login',None):
        #如果本来就没登录
        return redirect("/")
    #清空session中的内容
    request.session.flush()
    obj_cookies = redirect('/')
    # 删除用户和哈希值密码的cookies
    obj_cookies.delete_cookie('username')
    obj_cookies.delete_cookie('password')
    return obj_cookies

#密码哈希值加密
def hash_code(s,salt='mysite'):
    #sha256算法加密
    h = hashlib.sha256()
    s += salt 
    #update只接受字节串
    h.update(s.encode())
    return h.hexdigest()

#修改密码
def change_password(request):
    #只有在登录状态才会显示修改密码的按钮,所以这里不用判断用户登陆没
    if request.method == "POST":
        
        #加载修改密码的form表
        change_password_form = forms.ChangepasswordForm(request.POST)
        message = "所有字段都必须填写正确哦~"
        try:
            #获取此时登录的用户名
            username = request.session['user_name']
            #获取当前登录的用户对象
            user = models.User.objects.get(name=username)
        except:
            message = "无法获取当前用户名"
        # 获取数据
        if change_password_form.is_valid():
            #获取表格传入的数据
            old_password = change_password_form.cleaned_data['old_password']
            new_password1 = change_password_form.cleaned_data['new_password1']
            new_password2 = change_password_form.cleaned_data['new_password2']

            if new_password1 != new_password2:
                message = "两次输入的密码不同"
                return render(request, 'login/change_password.html', locals())
            elif hash_code(old_password) == hash_code(new_password1):
                message = "新老密码不能相同"
                return render(request, 'login/change_password.html', locals())
            elif len(new_password1) < 6 or len(new_password1) > 12:
                message = "密码长度在6-12个字符间"
                return render(request, 'login/change_password.html', locals())
            else:
                try:
                    #哈希值和数据库值对比
                    if user.password == hash_code(old_password):
                        #改变密码
                        user.password = hash_code(new_password1)
                        user.save()
                        return render(request, 'login/change_password_done.html', locals())
                    else:
                        message = "原密码不正确哦"
                        return render(request, 'login/change_password.html', locals())
                except:
                    message = "请填入正确的原密码"

        return render(request, "login/change_password.html", locals())

    change_password_form = forms.ChangepasswordForm()
    return render(request, 'login/change_password.html', locals())  

#确认邮件请求
def user_confirm(request):
    #获取请求类型
    type = request.GET.get('type', None)
    #获取确认码
    code = request.GET.get('code', None)
    message = ''
    now = datetime.datetime.now()

    if type == 'register':     
        try:
            #查看数据库中确认码一致的
            confirm = models.ConfirmString.objects.get(code=code)
            c_time = confirm.c_time 
        except:
            message = '您的注册邮件验证已被使用或无效,请重新申请邮件确认'
            return render(request, 'login/confirm.html', locals())

        #时间超时
        if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
            #删除数据表中的用户 级联删除
            confirm.user.delete()
            message = "您的邮件已经过期!请重新注册"
            return render(request, 'login/confirm.html', locals())
        else:
            #改变用户表中的邮箱验证状态
            confirm.user.has_confirmed = True 
            confirm.user.save()
            #从数据库中删除注册码
            confirm.delete()
            message = "感谢确认,请使用账户密码登录~"
            return render(request, 'login/confirm.html', locals())

    elif type == "reset":
        try:
            #查看数据库中确认码一致的
            confirm = models.Reset_ConfirmString.objects.get(code=code)
            c_time = confirm.c_time 
        except:
            message = '您的邮件确认已被使用或无效,请重新申请邮件确认'
            return render(request, 'login/confirm.html', locals())

        #时间超时
        if now > c_time + datetime.timedelta(settings.RESET_DAYS):  
            message = "您的重置密码邮件已过期!请再次重置密码"
            return render(request, 'login/reset_password.html', locals())
        else:
            #改变用户表中的重置密码状态
            confirm.user.reset_password = True
            confirm.user.save()
            #获取用户名
            request.session['user_name'] = confirm.user.name
            #删除重置码
            confirm.delete()
            message = "重置密码成功,请输入新密码"
            return render(request, 'login/reset_confirm.html', locals())



#重置密码邮箱验证
def reset_password(request):
    #重置密码只有在用户没登陆时才有按钮
    if request.method == "POST":
        #加载重置密码的form表
        reset_password_form = forms.ResetpasswordForm(request.POST)
        message = "所有字段都必须填写正确哦~"
        # 在form表中获取数据
        if reset_password_form.is_valid():
            email = reset_password_form.cleaned_data['email']
            try:       
                #判断邮箱在不在数据库中
                same_email_user = models.User.objects.filter(email=email)
            except:
                message = "获取不到用户的邮箱"
            #如果邮箱不存在
            if not same_email_user:
                message = "此邮箱未被注册"
            #邮箱存在
            else:
                #获取用户对象
                user = models.User.objects.get(email=email)
                #认证注册邮箱
                #创建确认码对象,user加盐
                code = make_confirm_string(user, 'Reset_ConfirmString')
                send_email(email, code, 'reset')
                message = "请前往注册邮箱,进行重置密码的邮箱认证~"
                #跳转到等待邮件确认页面
                hashkey = CaptchaStore.generate_key()
                image_url = captcha_image_url(hashkey)
                return render(request, 'login/reset_password_done.html', locals())
        #form表单自带验证不成功
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'login/reset_password.html', locals())

    reset_password_form = forms.ResetpasswordForm()
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    return render(request, 'login/reset_password.html', locals())

#让用户输入重置的新密码
def reset_password_ready(request):
    #只有在点击邮件中的链接验证成功后才会跳转到这里,所以这里不用判断用户登陆没
    if request.method == "POST":
        #获取用户名
        try:
            name = request.session.get('user_name')
            #获取用户对象
            user = models.User.objects.get(name=name)


            #判断是否开启重置密码服务
            if not user.reset_password:
                message = "您未申请重置密码"
                return render(request, 'login/confirm.html', locals())
        except:
            message = '无法获取要重置的用户'
        #加载重置新密码的form表
        reset_password_ready_form = forms.ResetpasswordreadyForm(request.POST)
        message = "所有字段都必须填写哦~"
        # 获取数据
        if reset_password_ready_form.is_valid():
            #获取表格传入的数据
            new_password1 = reset_password_ready_form.cleaned_data['new_password1']
            new_password2 = reset_password_ready_form.cleaned_data['new_password2']

            if new_password1 != new_password2:
                message = "两次输入的密码不同"
                return render(request, 'login/reset_password_ready.html', locals())

            elif len(new_password1) < 6 or len(new_password1) > 12:
                message = "密码长度在6-12个字符间"
                return render(request, 'login/reset_password_ready.html', locals())
            else:
                try:
                    #改变密码
                    user.password = hash_code(new_password1)
                    #将重置密码的选项改为false
                    user.reset_password = False
                    user.save()       
                             
                    return render(request, 'login/change_password_done.html', locals())
                except Exception as e:
                    message = "修改密码失败,请联系管理员"
                    print(e)
                    return render(request, 'login/reset_password_ready.html', locals())
        #form验证不成功
        return render(request, "login/reset_password_ready.html", locals())

    reset_password_ready_form = forms.ResetpasswordreadyForm()
    return render(request, 'login/reset_password_ready.html', locals()) 
                
#展示用户信息
def information(request):
    try:
        #获取此时登录的用户名
        username = request.session['user_name']
        #获取当前登录的用户对象
        user = models.User.objects.get(name=username)
    except:
        message = "无法获取当前用户名"    
    #性别字典
    gender = {'male':'男', 'female':'女', 'unkown':'不详'}

    name = username 
    email = user.email 
    sex = gender[user.sex]
    petname = user.petname
    pet_type = user.pet_type
    intro = user.intro
    photo = user.photo
    return render(request, 'login/information.html', locals())
    
        
#修改用户信息
def modify(request):
    try:
        #获取此时登录的用户名
        username = request.session['user_name']
        #获取当前登录的用户对象
        user = models.User.objects.get(name=username)
        #获取当前用户的头像
        photo = user.photo
        # print(user.name)
    except:
        message = "无法获取当前用户名"  
    # 如果提交了表单
    if request.method == "POST":
        
        modify_form = forms.ModifyForm(request.POST)
        message = "所有字段都必须填写哦~"
        # 获取数据
        print(modify_form.is_valid())
        if modify_form.is_valid():
            #获取表格传入的数据
            username = modify_form.cleaned_data['username']
            sex = modify_form.cleaned_data['sex']
            petname = modify_form.cleaned_data['petname']
            pet_type = modify_form.cleaned_data['pet_type']
            intro = modify_form.cleaned_data['intro']

            #用户名如果改变了
            if username != user.name:
                same_name_user = models.User.objects.filter(name=username)
                #如果用户名存在
                if same_name_user:
                    message = "用户名已存在,请重新输入"
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)
                    return render(request, 'login/modify.html', locals())
            if len(username) < 2 or len(username) > 15:
                message = "用户名长度必须在2-15字符间"
                hashkey = CaptchaStore.generate_key()
                image_url = captcha_image_url(hashkey)
                return render(request, 'login/modify.html', locals())
            #一切都ok时,改变数据库
            user.name = username
            user.sex = sex 
            user.petname = petname 
            user.pet_type = pet_type
            user.intro = intro
            #更新数据库数据
            user.save()

            return render(request, 'login/modify_done.html', locals())
        # 打印表单验证失败的原因
        else:
            print(modify_form.errors)

    # 如果是get请求
    #实例化对象 传入当前用户的信息为input默认值
    modify_form = forms.ModifyForm(initial={'username':user.name,
    'sex':user.sex,
    'petname':user.petname,
    'pet_type':user.pet_type,
    'intro':user.intro})

    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    return render(request, 'login/modify.html', locals()) 

#首页
def home(request):
    #判断有没有cookies
    judeg_cookies(request)
    #查询前三名销量的商品
    #导入另一个包中的models
    from polls import models as polls_models
    #只显示前三个
    pets = polls_models.Pets.objects.order_by("-pnumber").all()[:3]
    return render(request, 'login/home.html', locals())

#关于我们
def aboutus(request):
    return render(request, 'login/aboutus.html')

# 上传并裁剪图片
def head_photo(request):
    try:
        #获取此时登录的用户名
        username = request.session['user_name']
        #获取当前登录的用户对象
        user = models.User.objects.get(name=username)
        #从数据库中获取当前用户的头像的相对路径
        photo = user.photo

        # print(photo)
    except Exception as e:
        print('读取当前用户名错误:',e)
    return render(request, 'login/head_photo.html', locals())

# 取消csrf认证
@csrf_exempt
#处理裁剪图片的提交
def handing_head(request):
    try:
        #获取此时登录的用户名
        username = request.session['user_name']
        #获取当前登录的用户对象
        user = models.User.objects.get(name=username)
        #从数据库中获取当前用户的头像的相对路径
        photo = user.photo

        # print(photo)
    except Exception as e:
        print('读取当前用户名错误:',e)

    if request.method == 'POST':
        # 如果用户上传了头像
        if request.FILES.get('avatar_file', None):
            print('post请求接受')

            # 获取头像对象
            img = request.FILES['avatar_file']
            # 获取ajax返回的图片坐标
            data = request.POST['avatar_data']
            if img.size / 1024 > 700:
                return JsonResponse({"message": "原图片尺寸应小于900 X 1200 像素, 请重新上传。", })

            #数据库中的原图片路径
            current_avatar = user.photo
            # 根据传来的数据裁剪图片
            #传入原头像路径,本次头像对象,裁剪参数,用户id
            cropped_avatar = crop_image(current_avatar, img, data, user.id)



            #更新数据库中图片路径
            user.photo = cropped_avatar
            print('存入数据库的新图片:',user.photo)
            #保存更新
            user.save()
            print("图片路径:", user.photo.url)

            # 向前端返回一个json，result值是图片路径
            js_obj = {"result": user.photo.url}
            return JsonResponse(js_obj)

        else:
            return JsonResponse({"msg": "请重新上传。只能上传图片"})







#裁剪图片
def crop_image(current_avatar , file, data, uid):
    #自定义路径
    #文件后缀保留
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    print(file_name)
    #组合路径 以用户id为文件夹
    cropped_avatar = os.path.join(str(uid), "avatar", file_name)
    #相对media的路径
    file_path = os.path.join("media", str(uid), "avatar", file_name)

    # 获取Ajax发送的裁剪参数data，先用json解析。
    coords = json.loads(data)
    t_x = int(coords['x'])
    t_y = int(coords['y'])
    t_width = t_x + int(coords['width'])
    t_height = t_y + int(coords['height'])
    t_rotate = coords['rotate']

    # 裁剪图片,压缩尺寸为400*400。
    #打开原图片
    img = Image.open(file)
    #根据坐标裁剪
    crop_im = img.crop((t_x, t_y, t_width, t_height)).resize((400, 400), Image.ANTIALIAS).rotate(t_rotate)
    #去掉文件名,返回目录avatar
    directory = os.path.dirname(file_path)
    #如果用户目录下有avatar文件夹
    if os.path.exists(directory):
        crop_im.save(file_path)
    # 如果用户目录没有avatar文件夹
    else:
        os.makedirs(directory)
        crop_im.save(file_path)

    # 如果改变前数据库的头像路径不是默认头像，删除老头像图片, 节省空间
    if not current_avatar == os.path.join("avatar", "default.jpg"):
        #os.path.basename()返回文件名 根据数据库中存的图片途径 删除原头像
        current_avatar_path = os.path.join("media", str(uid), "avatar", os.path.basename(current_avatar.url))
        os.remove(current_avatar_path)
    #返回目前图片以用户id文件夹开始的路径
    return cropped_avatar


#重新发送注册邮件
def send_again_register(request):
    #只有在用户没登陆时才有重新发送注册邮件按钮
    if request.method == "POST":
        #加载重新发送邮件的表
        send_again_form = forms.SendAgainForm(request.POST)
        message = "所有字段都必须填写正确哦~"
        # 在form表中获取数据
        if send_again_form.is_valid():
            email = send_again_form.cleaned_data['email']
            password = send_again_form.cleaned_data['password']
            try:
                # 判断邮箱在不在数据库中
                same_email_user = models.User.objects.filter(email=email)
            except:
                message = "获取不到用户的邮箱"
            # 如果邮箱不存在
            if not same_email_user:
                message = "此邮箱未被注册"
                # hashkey = CaptchaStore.generate_key()
                # image_url = captcha_image_url(hashkey)
                # return render(request, 'login/send_again_register.html', locals())
            # 邮箱存在
            else:
                # 获取用户对象
                user = models.User.objects.get(email=email)
                #获取用户id
                user_id = user.id
                #如果用户输入的密码和数据库中密码一致
                if user.password == hash_code(password):
                    try:
                        #找到确认码数据表中用户对应的对象
                        confirm = models.ConfirmString.objects.get(user=user_id)
                        # 如果确认码存在
                        if confirm:
                            # 从数据库中删除注册码
                            confirm.delete()
                    #如果没有
                    except Exception as e:
                        print('查询确认码失败:', e)

                    #创建新的注册确认码
                    code = make_confirm_string(user, 'ConfirmString')
                    try:
                        send_email(email, code, 'register')
                    except Exception as e:
                        message = "邮件发送失败,请联网或换一个邮箱重新注册"
                        print('重新发送注册验证邮件拦截异常')
                        # 删除数据库中对应的用户
                        models.User.objects.filter(name=username).delete()
                        # 返回注册界面
                        hashkey = CaptchaStore.generate_key()
                        image_url = captcha_image_url(hashkey)
                        return render(request, 'login/register.html', locals())
                    #成功发送邮件后
                    message = "请前往注册邮箱,进行邮箱认证~"
                    # 跳转到等待邮件确认页面
                    return render(request, 'login/confirm.html', locals())
                #如果用户输入的密码错误
                else:
                    message = "密码错误,重新发送邮件失败"
            #如果密码错误或者邮箱不存在
            hashkey = CaptchaStore.generate_key()
            image_url = captcha_image_url(hashkey)
            return render(request, 'login/send_again_register.html', locals())
        #如果form验证失败
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'login/send_again_register.html', locals())
    #如果是get请求
    send_again_form = forms.SendAgainForm()
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    return render(request, 'login/send_again_register.html', locals())


