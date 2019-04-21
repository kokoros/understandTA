from django.db import models


# Create your models here.
class Productinfo(models.Model):
    # Pid=models.AutoField
    Pname = models.CharField(max_length=100)
    Pdescribe = models.CharField(max_length=225)
    Pprice = models.FloatField()
    Ptime = models.CharField(max_length=100)
    Ptype = models.CharField(max_length=100)
    Pamount = models.IntegerField()
    Pphoto = models.CharField(max_length=200)
    # def __str__(self):
    #     return ll(self.Pname,self.Pdescribe,self.Pprice,self.Ptime,self.Ptype,self.Pamount,self.Pphoto)


class Pets(models.Model):
    pname = models.CharField(max_length=200)
    ptype = models.CharField(max_length=200)
    pdescribe = models.TextField(null=True)
    pnumber = models.IntegerField(default=0, null=True)
    ppath = models.CharField(max_length=200, null=True)
    ptime = models.CharField(max_length=200, null=True)
    ptypeid = models.IntegerField(null=True)
    pspareint = models.IntegerField(null=True)
    psparestr = models.CharField(max_length=200, null=True)
    pdesc = models.TextField(null=True)
    pprice = models.FloatField(null=True)
    penable = models.IntegerField(default=0, null=True)


class Collect(models.Model):
    pid = models.IntegerField()
    uname = models.CharField(max_length=200)
    cname = models.CharField(max_length=200)
    ctype = models.CharField(max_length=200)
    cdescribe = models.TextField(null=True)
    cnumber = models.IntegerField(default=0, null=True)
    cpath = models.CharField(max_length=200, null=True)
    ctime = models.CharField(max_length=200, null=True)
    ctypeid = models.IntegerField(null=True)
    csparestr = models.CharField(max_length=200, null=True)
    cdesc = models.TextField(null=True)
    cprice = models.FloatField(null=True)
    callprice = models.FloatField(null=True)
    cenable = models.IntegerField(default=0, null=True)


class Order(models.Model):
    cid = models.IntegerField()
    uname = models.CharField(max_length=200)
    oname = models.CharField(max_length=200)
    oprice = models.FloatField()
    onum = models.IntegerField()
    oaddress = models.CharField(max_length=200)
    ouser = models.CharField(max_length=200)
    ophone = models.CharField(max_length=200, null=True)
    ostatue = models.IntegerField()
    odesc = models.TextField(null=True)
    otime = models.CharField(max_length=200, null=True)
    oenable = models.IntegerField(default=0, null=True)
    opath = models.CharField(max_length=200, null=True)
    ohandle1=models.CharField(max_length=200,null=True) #订单支付
    ohandle2=models.CharField(max_length=200,null=True) #订单删除
    ohandle3=models.CharField(max_length=200,null=True)#确认收货
    ohandle4=models.CharField(max_length=200,null=True)#退货order;
