from django.shortcuts import render, redirect
from login import models
from login import forms
import hashlib
import datetime
from django.conf import settings
#导入文件系统
from django.core.files.storage import FileSystemStorage
import os
#导入验证码模块
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
#导入Q查询
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request, 'login/index.html')

#登录
def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "所有字段都必须填写哦~"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                # 判断是否是邮箱或者用户名
                user = models.User.objects.get(Q(name=username) | Q(email=username))
                print(user)
                #判断是否通过邮件确认
                if not user.has_confirmed:
                    message = "您还未通过邮件确认注册"
                    return render(request,'login/login.html', locals())
                #哈希值和数据库值对比
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    #把重置密码状态改为false

                    return redirect('/index/')
                else:
                    message = "密码不正确哦"
            except:
                message = "用户名或邮箱不存在~"
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, "login/login.html", locals())

    login_form = forms.UserForm()
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    return render(request, 'login/login.html', locals())

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
                return render(request, 'login/register.html', locals())
            elif len(password1) < 6 or len(password1) > 12:
                message = "密码长度在6-12个字符间"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                #如果用户名存在
                if same_name_user:
                    message = "用户名已存在,请重新输入"
                    return render(request,'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                #如果邮箱存在
                if same_email_user:
                    message = "邮箱已被注册,请换一个邮箱注册"
                    return render(request, 'login/register.html', locals())
                #一切都ok时
                new_user = models.User()
                new_user.name = username 
                #使用加密密码
                new_user.password = hash_code(password1)
                new_user.email = email 
                new_user.sex = sex 
                new_user.pet_type = pet_type 
                new_user.intro = intro 
                #如果用户上传的头像
                if request.FILES.get('photo', None):
                    # 获取头像
                    photo_obj = request.FILES['photo']
                    #文件格式 正则
                    import re
                    l = re.split(r'\.',photo_obj.name)
                    photo_type = l[-1]
                    photo_name = new_user.name + '.' + photo_type
                    #存储文件
                    try:
                        destination = open(os.path.join("/home/koro/mysite/media/photo",photo_name),"wb+")
                        for chunk in photo_obj.chunks():
                            destination.write(chunk)
                        
                    except Exception as e:
                        print('存储文件失败:',e)
                    finally:
                        destination.close()
                        photo_obj.close()

                    # 拼接路径
                    photo = "photo/" + new_user.name + '.' + photo_type
                    #保存图片路径到数据库
                    new_user.photo = photo
                new_user.save()

                #认证注册邮箱
                code = make_confirm_string(new_user, 'ConfirmString')
                send_email(email, code, 'register')
                message = "请前往注册邮箱,进行邮箱认证~"
                #跳转到等待邮件确认页面
                return render(request, 'login/confirm.html', locals())

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

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
        '''.format('127.0.0.1:8000', code, string , settings.RESET_DAYS)
    #试图发送邮件
    try:
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print('邮件发送失败:',e)


def logout(request):
    if not request.session.get('is_login',None):
        #如果本来就没登录
        return redirect("/index/")
    #清空session中的内容
    request.session.flush()
    return redirect("/index/")

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
        message = "所有字段都必须填写哦~"
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
            message = '您的邮件确认已被使用或无效,请重新申请邮件确认'
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
                return render(request, 'login/reset_password_done.html', locals())

    reset_password_form = forms.ResetpasswordForm()
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
                except:
                    message = "修改密码失败,请联系管理员"
                    return render(request, 'login/reset_password_ready.html', locals())
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
                    return render(request, 'login/modify.html', locals())
            #一切都ok时,改变数据库
            user.name = username
            user.sex = sex 
            user.petname = petname 
            user.pet_type = pet_type
            user.intro = intro 


            # 如果用户上传了头像
            if request.FILES.get('new_photo', None):
                # 获取头像
                photo_obj = request.FILES['new_photo']
                #获取文件格式 正则
                import re
                l = re.split(r'\.',photo_obj.name)
                photo_type = l[-1]
                photo_name = user.name + '.' + photo_type
                # 替换头像文件
                try:
                    destination = open(os.path.join("/home/koro/mysite/media/photo", photo_name),"wb+")
                    for chunk in photo_obj.chunks():
                        destination.write(chunk)
                        
                except Exception as e:
                    print('存储文件失败:',e)
                finally:
                    destination.close()
                    photo_obj.close()
                # 拼接路径
                photo = "photo/" + user.name + '.' + photo_type
                #保存图片路径到数据库
                user.photo = photo
            #更新数据库数据
            #数据库中的头像路径也要改变
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

    return render(request, 'login/modify.html', locals()) 

def home(request):
    return render(request, 'login/home.html')

