from django import forms
from django.forms import ModelForm
from .models import fm_utrans
class AccountTypeForm(forms.Form):
    c  = [("1","Main"),("2","BIRAC")]
    choices = forms.ChoiceField(choices=c, label="Select Account Type")

class TransferMoneyForm(forms.ModelForm):
    class Meta:
        model = fm_utrans
        exclude = ('utranID','txnID','utranConfirmed','utranSender')
    def save(self,user):
        obj = super().save(commit = False)
        obj.utranSender = user
        obj.save()
        return obj
