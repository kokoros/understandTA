from django import forms 
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名/邮箱",max_length=128,widget=forms.TextInput(attrs={'class':'lowin-input', 'placeholder' : '请输入用户名或邮箱'}))
    password = forms.CharField(label="密码",max_length=256, widget=forms.PasswordInput(attrs={'class':'lowin-input', 'placeholder'  :'请输入密码', 'autocomplete': 'current-password', 'id': 'password'}))
    captcha = CaptchaField(label="验证码")



class RegisterForm(forms.Form):
    gender = (
        ('male','男'),
        ('female','女'),
        ('unkown','不详')
    )

    username = forms.CharField(label="用户名(可以输入中文)",max_length=128,widget=forms.TextInput(attrs={'class': 'lowin-input','placeholder' : '请输入用户名', 'id': 'user_name'}))
    password1 = forms.CharField(label="密码",max_length=256,widget=forms.PasswordInput(attrs={'class': 'lowin-input', 'placeholder' : '请输入密码','id':'password1'}))
    password2 = forms.CharField(label="确认密码",max_length=256,widget=forms.PasswordInput(attrs={'class': 'lowin-input', 'placeholder' : '请再次输入密码','id':'password2'}))
    
    email = forms.EmailField(label="邮箱地址(注册后不可更改邮箱,请谨慎填写)",widget=forms.EmailInput(attrs={'class':'lowin-input', 'placeholder' : '请输入邮箱', 'id': 'user_email'}))

    sex = forms.ChoiceField(label="性别",choices=gender,initial="unkown")
    petname = forms.CharField(label="宠物名",max_length=128,initial="不详",widget=forms.TextInput(attrs={'class':'lowin-input', 'placeholder' : '请输入主子名'}))
    pet_type = forms.CharField(label="宠物种类",max_length=128,initial="不详",widget=forms.TextInput(attrs={'class':'lowin-input', 'placeholder' : '请输入主子种类'}))
    intro = forms.CharField(label="个性签名",max_length=1024,initial="不详",widget=forms.TextInput(attrs={'class':'lowin-input', 'placeholder' : '请输入个性签名'}))
    # photo = forms.CharField(label="头像",max_length=1024,initial="不详",widget=forms.TextInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label="验证码")

class ChangepasswordForm(forms.Form):
    old_password = forms.CharField(label="原密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'lowin-input', 'placeholder' : '请输入旧密码', 'id': 'password'}))
    new_password1 = forms.CharField(label="新密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'lowin-input', 'placeholder' : '请输入新密码', 'id': 'password1'}))
    new_password2 = forms.CharField(label="确认新密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'lowin-input', 'placeholder' : '请再次输入新密码', 'id': 'password2'}))

#重置密码的视图表
class ResetpasswordForm(forms.Form):
    email = forms.EmailField(label="邮箱地址",widget=forms.EmailInput(attrs={'class':'lowin-input', 'placeholder': '请输入邮箱'}))
    captcha = CaptchaField(label="验证码")

#确认邮箱后,让用户输入新密码的视图表
class ResetpasswordreadyForm(forms.Form):
    new_password1 = forms.CharField(label="新密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'lowin-input', 'placeholder' : '请输入新密码'}))
    new_password2 = forms.CharField(label="确认新密码",max_length=256,widget=forms.PasswordInput(attrs={'class':'lowin-input', 'placeholder' : '请再次输入新密码'}))

#展示用户信息并可修改
class ModifyForm(forms.Form):
    gender = (
        ('male','男'),
        ('female','女'),
        ('unkown','不详')
    )
    
    username = forms.CharField(label="用户名",max_length=128,widget=forms.TextInput(attrs={'class':'lowin-input', 'id': 'user_name'}))
    sex = forms.ChoiceField(label="性别",choices=gender)
    petname = forms.CharField(label="宠物名",max_length=128,widget=forms.TextInput(attrs={'class':'lowin-input'}))
    pet_type = forms.CharField(label="宠物种类",max_length=128,widget=forms.TextInput(attrs={'class':'lowin-input'}))
    intro = forms.CharField(label="个性签名",max_length=1024,widget=forms.TextInput(attrs={'class':'lowin-input'}))
    captcha = CaptchaField(label="验证码")

#重新发送邮件表
class SendAgainForm(forms.Form):
    email = forms.EmailField(label="邮箱地址",widget=forms.EmailInput(attrs={'class':'lowin-input', 'placeholder': '请输入邮箱'}))
    password = forms.CharField(label="密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'lowin-input', 'placeholder': '请输入密码'}))
    captcha = CaptchaField(label="验证码")