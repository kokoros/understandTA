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
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 
    #魔法方法,让上面的代码能被Django识别
    class Meta:
        #按时间倒着排序
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
