from django.shortcuts import render,redirect
from login import models
from login import forms

# Create your views here.

def index(request):
    pass
    return render(request, 'login/index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "所有字段都必须填写哦~"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确哦"
            except:
                message = "用户名不存在~"
        return render(request, "login/login.html", locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html',locals())

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
            photo = register_form.cleaned_data['photo']
        if password1 != password2:
            message = "两次输入的密码不同"
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
                message = "邮箱已存在,请换一个邮箱注册"
                return render(request, 'login/register.html', locals())
            #一切都ok时
            new_user = models.User()
            new_user.name = username 
            new_user.password = password1
            new_user.email = email 
            new_user.sex = sex 
            new_user.pet_type = pet_type 
            new_user.intro = intro 
            new_user.photo = photo
            new_user.save()
            #自动跳转到登录页面
            return redirect('/login/')
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login',None):
        #如果本来就没登录
        return redirect("/index/")
    #清空session中的内容
    request.session.flush()
    return redirect("/index/")