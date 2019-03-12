from django.shortcuts import render,redirect
from login import models
from login import forms

# Create your views here.

def index(request):
    pass
    return render(request, 'login/index.html')

def login(request):
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "所有字段都必须填写哦~"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    return redirect('/index/')
                else:
                    message = "密码不正确哦"
            except:
                message = "用户名不存在~"
        return render(request, "login/login.html", locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html',locals())

def register(request):
    pass 
    return render(request, 'login/register.html')

def logout(request):
    pass 
    return redirect("/index/")