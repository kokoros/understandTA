from django.db import models

# Create your models here.

class User(models.Model):

    gender = (
        ('male','男'),
        ('female','女'),
        ('unkown','不详')
    )

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender, default="不详")
    petname = models.CharField(max_length=128,default='不详')
    pet_type = models.CharField(max_length=128,default="不详")
    intro = models.CharField(max_length=1024,default="你猜")
    photo = models.CharField(max_length=1024,default="太帅无法显示")
    c_time = models.DateTimeField(auto_now_add=True)
    # 默认未进行邮箱注册确认
    has_confirmed = models.BooleanField(default=False)
    #默认不开启重置密码服务
    reset_password = models.BooleanField(default=False)

    def __str__(self):
        return self.name 
    #魔法方法,让上面的代码能被Django识别
    class Meta:
        #按时间倒着排序
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"

#创建一张用户是否邮箱确认注册的新的数据库表
class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    # 外键 级联删除
    user = models.OneToOneField('User',on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":  " + self.code 
    
    #魔法方法
    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

#创建一张用户申请重置密码的数据库表
class Reset_ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    # 外键 级联删除
    user = models.OneToOneField('User',on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":  " + self.code 
    
    #魔法方法
    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"