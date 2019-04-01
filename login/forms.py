from django import forms 
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="密码",max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label="验证码")



class RegisterForm(forms.Form):
    gender = (
        ('male','男'),
        ('female','女'),
        ('unkown','不详')
    )

    username = forms.CharField(label="用户名",max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="确认密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    email = forms.EmailField(label="邮箱地址",widget=forms.EmailInput(attrs={'class':'form-control'}))

    sex = forms.ChoiceField(label="性别",choices=gender,initial="unkown")
    petname = forms.CharField(label="宠物名",max_length=128,initial="不详",widget=forms.TextInput(attrs={'class':'form-control'}))
    pet_type = forms.CharField(label="宠物种类",max_length=128,initial="不详",widget=forms.TextInput(attrs={'class':'form-control'}))
    intro = forms.CharField(label="简介",max_length=1024,initial="不详",widget=forms.TextInput(attrs={'class':'form-control'}))
    # photo = forms.CharField(label="头像",max_length=1024,initial="不详",widget=forms.TextInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label="验证码")

class ChangepasswordForm(forms.Form):
    old_password = forms.CharField(label="原密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(label="新密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))     
    new_password2 = forms.CharField(label="确认新密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))     

#重置密码的视图表
class ResetpasswordForm(forms.Form):
    email = forms.EmailField(label="邮箱地址",widget=forms.EmailInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label="验证码")

#确认邮箱后,让用户输入新密码的视图表
class ResetpasswordreadyForm(forms.Form):
    new_password1 = forms.CharField(label="新密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))     
    new_password2 = forms.CharField(label="确认新密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))   

#展示用户信息并可修改
class ModifyForm(forms.Form):
    gender = (
        ('male','男'),
        ('female','女'),
        ('unkown','不详')
    )
    
    username = forms.CharField(label="用户名",max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label="性别",choices=gender)
    petname = forms.CharField(label="宠物名",max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    pet_type = forms.CharField(label="宠物种类",max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    intro = forms.CharField(label="简介",max_length=1024,widget=forms.TextInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label="验证码")

