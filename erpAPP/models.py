from django.db import models
# Create your models here.
class csv_model(models.Model):
    trans_account = models.IntegerField()
    trans_id = models.CharField(max_length=20,primary_key=True)
    trans_date = models.DateField(auto_now=False,auto_now_add=False,null=False,blank=False)
    trans_posted_date = models.DateField(auto_now=False,auto_now_add=False,null=False,blank=False)
    trans_cheque = models.CharField(max_length=20)
    trans_desc = models.CharField(max_length=100)
    cr_or_dr = models.CharField(max_length=2)
    value = models.FloatField()
    balance = models.FloatField()
    def __str__(self):
        return self.trans_id
