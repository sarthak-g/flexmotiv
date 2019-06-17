from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class fm_txn(models.Model):
    txnID = models.CharField(max_length=20,primary_key=True)
    accID = models.IntegerField(default=0)
    txnDate = models.DateField(auto_now=False,auto_now_add=False,null=False,blank=False)
    txnPostedDate = models.DateField(auto_now=False,auto_now_add=False,null=False,blank=False)
    txnCheque = models.IntegerField()
    txnDir = models.CharField(max_length=1)
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
    utanDate = models.DateField(auto_now_add=True)
    utranID = models.IntegerField(null=True)
    txnID = models.IntegerField(null=True)
    utranDesc = models.CharField(max_length=50,verbose_name='Description')
    utranValue = models.IntegerField(verbose_name='Amount',null=True)
    utranConfirmed = models.CharField(max_length=1,default='N')
    utranSender = models.CharField(max_length=10,default='no')
    utranReceiver = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Receiver')
    def get_absolute_url(self):
        return reverse('transferMoney')
