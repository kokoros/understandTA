from django import forms

from gellary.models import *

class UserForm(forms.ModelForm):
    pname = forms.CharField(label='用户名',required=True)
    photo = forms.CharField(label='头像',required=True)
    pdate = forms.CharField(label='注册时间',required=True)
    ptype = forms.CharField(label='种类',required=True)
    psex = forms.CharField(label='性别',required=True)
    page = forms.CharField(label='年龄',required=True)
    pintro = forms.CharField(label='介绍',required=True)
    pwords = forms.CharField(label='留言',required=True)
    class Meta:
        model = User
        fields = ('pname','photo','pdate','ptype','psex','page','pintro','pwords')