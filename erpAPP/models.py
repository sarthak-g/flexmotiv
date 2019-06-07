from django.db import models
from djchoices import DjangoChoices,ChoiceItem


# Create your models here.
class csv_fm_txn(models.Model):
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

class CSVfileStorage(models.Model):
    txnAuditFileStorage = models.FileField(upload_to="file_link",max_length=100,unique=True)
