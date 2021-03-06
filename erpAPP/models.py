from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class fm_user_extend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uopeningBalance = models.FloatField(default=0)
    uBalance = models.FloatField(default=0)
    uUnconfirmed = models.FloatField(default=0)
    uDeclined = models.FloatField(default=0)

class fm_txn(models.Model):
    txnID = models.CharField(max_length=20,primary_key=True)
    accID = models.IntegerField(default=0)
    txnDate = models.DateField(auto_now=False,auto_now_add=False,null=False,blank=False)
    txnPostedDate = models.DateField(auto_now=False,auto_now_add=False,null=False,blank=False)
    txnCheque = models.FloatField()
    txnDir = models.CharField(max_length=2)
    txnDesc = models.CharField(max_length=100)
    txnValue = models.FloatField()
    txnBalance = models.FloatField()
    txnAuditFile = models.URLField(max_length=200)
    txnType = models.CharField(max_length=1,default='U')
    txnAccounted = models.BooleanField(default=0)
    txnAudited = models.BooleanField(default=0)
    prID = models.IntegerField(null=True)
    ptcID = models.IntegerField(null=True)
    bhlID = models.IntegerField(null=True)
    transc_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.txnID

# class CSVfileStorage(models.Model):
#     txnAuditFileStorage = models.FileField(upload_to="file_link",max_length=100,unique=True)


class fm_utrans(models.Model):
    utranDate = models.DateField(auto_now_add=True)
    txnID = models.CharField(max_length=20,null=True)
    utranDesc = models.CharField(max_length=50,verbose_name='Description')
    utranValue = models.FloatField(verbose_name='Amount',null=True)
    utranConfirmed = models.CharField(max_length=1,default='N')
    utranSender = models.CharField(max_length=10,default='no')
    utranReceiver = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Receiver')
    def get_absolute_url(self):
        return reverse('transferMoney')

class fm_project(models.Model):
    prTitle = models.CharField(max_length=50,verbose_name='Project Title')
    prDesc = models.CharField(max_length=200,verbose_name = 'Project Description')
    prManagers_1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='first_project_manager',verbose_name ='Project Manager 1')
    prManagers_2 = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL,related_name='second_project_manager',verbose_name ='Project Manager 2')
    prManagers_3 = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL,related_name='third_project_manager',verbose_name ='Project Manager 3')
    prManagers_4 = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL,related_name='fourth_project_manager',verbose_name ='Project Manager 4')
    prManagers_5 = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL,related_name='fifth_project_manager',verbose_name ='Project Manager 5')
    prManagers_6 = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL,related_name='sixth_project_manager',verbose_name ='Project Manager 6')
    prBudget = models.FloatField(default=0,verbose_name='Total Budget')
    prBalance = models.FloatField(default=0,verbose_name='Balance of budget')
    def __str__(self):
        return self.prTitle
class fm_budgethead(models.Model):
    prID = models.ForeignKey(fm_project,on_delete = models.CASCADE)
    bhTitle = models.CharField(max_length=50)
    bhLimit = models.FloatField(default=0)
    bhBalance = models.FloatField(default=0)
    bhBalanceDate = models.DateField(auto_now=True)
    def __str__(self):
        return self.bhTitle


class fm_ptcform(models.Model):
    uID = models.ForeignKey(User,on_delete=models.CASCADE)
    ptcValue = models.FloatField(default=0)
    ptcType = models.CharField(max_length=40,null=True)
    prID = models.ForeignKey(fm_project,on_delete=models.CASCADE)
    ptcDate = models.DateField(auto_now=True)
    ptcApproved = models.BooleanField(default=0)
    ptcApprovedBy = models.CharField(max_length=50,null=True)
    txnID = models.ForeignKey(fm_txn,null=True,on_delete=models.SET_NULL)
    ptcType_D_E = models.CharField(max_length=1,null=True)
    class Meta:
        get_latest_by = 'uID'

class fm_ptctrans(models.Model):
    ptctransDate = models.DateField(auto_now=False,auto_now_add=False)
    ptcID = models.ForeignKey(fm_ptcform,on_delete=models.CASCADE)
    ptctransValue = models.FloatField()
    ptctransInvoiceStatus = models.CharField(max_length=1)
    ptctransInvoiceFile = models.FileField(upload_to="InvoiceFile",max_length=100,unique=True)
    ptctransHead = models.ForeignKey(fm_budgethead,on_delete=models.CASCADE)
    prID = models.ForeignKey(fm_project,on_delete=models.CASCADE)
    uID = models.ForeignKey(User,on_delete=models.CASCADE)
    ptctransApproved = models.BooleanField(default=0)
    ptctransApprovedBy = models.CharField(max_length=50,null=True)
    ptcVendor = models.CharField(max_length=50)
    ptcDesc = models.CharField(max_length=200)
    ptcAccounted = models.BooleanField(default=0)
    ptcAudited = models.BooleanField(default=0)
