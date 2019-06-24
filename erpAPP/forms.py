from django import forms
from django.forms import ModelForm
from .models import fm_utrans,fm_project,fm_budgethead,fm_ptctrans
from django.contrib.auth.models import User
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

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = fm_project
        exclude = ('prBudget','prBalance')

    def __init__(self, *args,**kwargs):
        super (AddProjectForm,self ).__init__(*args,**kwargs)
        self.fields['prManagers_1'].queryset = User.objects.filter(groups__name='projectmanager')
        self.fields['prManagers_2'].queryset = User.objects.filter(groups__name='projectmanager')
        self.fields['prManagers_3'].queryset = User.objects.filter(groups__name='projectmanager')
        self.fields['prManagers_4'].queryset = User.objects.filter(groups__name='projectmanager')
        self.fields['prManagers_5'].queryset = User.objects.filter(groups__name='projectmanager')
        self.fields['prManagers_6'].queryset = User.objects.filter(groups__name='projectmanager')

class ProjectBudgetForm(forms.Form):
    title = forms.CharField(max_length=50)
    Limit = forms.IntegerField()
    Balance = forms.IntegerField()
class ProjectBudgetForm2(forms.Form):
    title2 = forms.CharField(max_length=50,required=False)
    Limit2 = forms.IntegerField(required=False)
    Balance2 = forms.IntegerField(required=False)
class ProjectBudgetForm3(forms.Form):
    title3 = forms.CharField(max_length=50,required=False)
    Limit3 = forms.IntegerField(required=False)
    Balance3 = forms.IntegerField(required=False)
class ProjectBudgetForm4(forms.Form):
    title4 = forms.CharField(max_length=50,required=False)
    Limit4 = forms.IntegerField(required=False)
    Balance4 = forms.IntegerField(required=False)
class ProjectBudgetForm5(forms.Form):
    title5 = forms.CharField(max_length=50,required=False)
    Limit5 = forms.IntegerField(required=False)
    Balance5 = forms.IntegerField(required=False)
class ProjectBudgetForm6(forms.Form):
    title6 = forms.CharField(max_length=50,required=False)
    Limit6 = forms.IntegerField(required=False)
    Balance6 = forms.IntegerField(required=False)
class ProjectBudgetForm7(forms.Form):
    title7 = forms.CharField(max_length=50,required=False)
    Limit7 = forms.IntegerField(required=False)
    Balance7 = forms.IntegerField(required=False)
class ProjectBudgetForm8(forms.Form):
    title8 = forms.CharField(max_length=50,required=False)
    Limit8 = forms.IntegerField(required=False)
    Balance8 = forms.IntegerField(required=False)
class ProjectBudgetForm9(forms.Form):
    title9 = forms.CharField(max_length=50,required=False)
    Limit9 = forms.IntegerField(required=False)
    Balance9 = forms.IntegerField(required=False)
class ProjectBudgetForm10(forms.Form):
    title10 = forms.CharField(max_length=50,required=False)
    Limit10 = forms.IntegerField(required=False)
    Balance10 = forms.IntegerField(required=False)
class ptcprojectform(forms.ModelForm):
    class Meta:
        model = fm_ptctrans
        fields = ('prID',)
