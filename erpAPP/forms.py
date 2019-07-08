from django import forms
from django.forms import ModelForm
from .models import fm_utrans,fm_project,fm_budgethead,fm_ptcform,fm_ptctrans
from django.contrib.auth.models import User
import datetime
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

class ptcprojectform(forms.Form):
    prID = forms.ModelChoiceField(queryset=fm_project.objects.all(),label="Select project")
class ptctransform(forms.Form):
    Date_ptcform = forms.DateField(label="Date in (YYYY-MM-DD)")
    Vendor = forms.CharField(max_length=50,label="Vendor")
    Description = forms.CharField(max_length=200,label="Desc")
    Value = forms.IntegerField(label="Value")
    Budgets = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices = forms.ChoiceField(choices=c, label="Invoice Status")
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform, self).__init__(*args,**kwargs)
        self.fields["Budgets"].queryset = budget_queryset
    ##Is there any particular file format for Invoice

class ptctransform2(forms.Form):
    Date_ptcform2 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor2 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description2 = forms.CharField(max_length=200,required=False,label="Desc")
    Value2 = forms.IntegerField(required=False,label="Value")
    Budgets2 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices2 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform2, self).__init__(*args,**kwargs)
        self.fields["Budgets2"].queryset = budget_queryset
class ptctransform3(forms.Form):
    Date_ptcform3 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor3 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description3 = forms.CharField(max_length=200,required=False,label="Desc")
    Value3 = forms.IntegerField(required=False,label="Value")
    Budgets3 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices3 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform3, self).__init__(*args,**kwargs)
        self.fields["Budgets3"].queryset = budget_queryset
class ptctransform4(forms.Form):
    Date_ptcform4 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor4 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description4 = forms.CharField(max_length=200,required=False,label="Desc")
    Value4 = forms.IntegerField(required=False,label="Value")
    Budgets4 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices4 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform4, self).__init__(*args,**kwargs)
        self.fields["Budgets4"].queryset = budget_queryset
class ptctransform5(forms.Form):
    Date_ptcform5 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor5 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description5 = forms.CharField(max_length=200,required=False,label="Desc")
    Value5 = forms.IntegerField(required=False,label="Value")
    Budgets5 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices5 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform5, self).__init__(*args,**kwargs)
        self.fields["Budgets5"].queryset = budget_queryset
class ptctransform6(forms.Form):
    Date_ptcform6 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor6 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description6 = forms.CharField(max_length=200,required=False,label="Desc")
    Value6 = forms.IntegerField(required=False,label="Value")
    Budgets6 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices6 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform6, self).__init__(*args,**kwargs)
        self.fields["Budgets6"].queryset = budget_queryset
class ptctransform7(forms.Form):
    Date_ptcform7 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor7 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description7 = forms.CharField(max_length=200,required=False,label="Desc")
    Value7 = forms.IntegerField(required=False,label="Value")
    Budgets7 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices7 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform7, self).__init__(*args,**kwargs)
        self.fields["Budgets7"].queryset = budget_queryset
class ptctransform8(forms.Form):
    Date_ptcform8 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor8 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description8 = forms.CharField(max_length=200,required=False,label="Desc")
    Value8 = forms.IntegerField(required=False,label="Value")
    Budgets8 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices8 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform8, self).__init__(*args,**kwargs)
        self.fields["Budgets8"].queryset = budget_queryset
class ptctransform9(forms.Form):
    Date_ptcform9 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor9 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description9 = forms.CharField(max_length=200,required=False,label="Desc")
    Value9 = forms.IntegerField(required=False,label="Value")
    Budgets9 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices9 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform9, self).__init__(*args,**kwargs)
        self.fields["Budgets9"].queryset = budget_queryset
class ptctransform10(forms.Form):
    Date_ptcform10 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor10 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description10 = forms.CharField(max_length=200,required=False,label="Desc")
    Value10 = forms.IntegerField(required=False,label="Value")
    Budgets10 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices10 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform10, self).__init__(*args,**kwargs)
        self.fields["Budgets10"].queryset = budget_queryset
class ptctransform11(forms.Form):
    Date_ptcform11 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor11 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description11 = forms.CharField(max_length=200,required=False,label="Desc")
    Value11 = forms.IntegerField(required=False,label="Value")
    Budgets11 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices11 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform11, self).__init__(*args,**kwargs)
        self.fields["Budgets11"].queryset = budget_queryset
class ptctransform12(forms.Form):
    Date_ptcform12 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor12 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description12 = forms.CharField(max_length=200,required=False,label="Desc")
    Value12 = forms.IntegerField(required=False,label="Value")
    Budgets12 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices12 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform12, self).__init__(*args,**kwargs)
        self.fields["Budgets12"].queryset = budget_queryset
class ptctransform13(forms.Form):
    Date_ptcform13 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor13 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description13 = forms.CharField(max_length=200,required=False,label="Desc")
    Value13 = forms.IntegerField(required=False,label="Value")
    Budgets13 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices13 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform13, self).__init__(*args,**kwargs)
        self.fields["Budgets13"].queryset = budget_queryset
class ptctransform14(forms.Form):
    Date_ptcform14 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor14 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description14 = forms.CharField(max_length=200,required=False,label="Desc")
    Value14 = forms.IntegerField(required=False,label="Value")
    Budgets14 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices14 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform14, self).__init__(*args,**kwargs)
        self.fields["Budgets14"].queryset = budget_queryset
class ptctransform15(forms.Form):
    Date_ptcform15 = forms.DateField(label="Date in (YYYY-MM-DD)",required=False)
    Vendor15 = forms.CharField(max_length=50,required=False,label="Vendor")
    Description15 = forms.CharField(max_length=200,required=False,label="Desc")
    Value15 = forms.IntegerField(required=False,label="Value")
    Budgets15 = forms.ModelChoiceField(queryset=fm_budgethead.objects.all(),required=False,label="Budgets")
    c  = [("Y","Invoice Available"),("P","Invoice Pending"),("N","Invoice Not Available")]
    choices15 = forms.ChoiceField(choices=c, label="Invoice Status",required=False)
    # InvoiceFile = forms.FileField(label="Upload Invoice")
    def __init__(self,budget_queryset,*args,**kwargs):
        super(ptctransform15, self).__init__(*args,**kwargs)
        self.fields["Budgets15"].queryset = budget_queryset

class CheckStatementForm(forms.Form):
    c  = [("1","Main"),("2","BIRAC")]
    choices = forms.ChoiceField(choices=c, label="Select Account Type")
    year =[(str(i),str(i)) for i in range(2017,datetime.datetime.now().year + 1)]
    choices2 = forms.ChoiceField(choices=year, label="Year")
    month = [("01","Jan"),("02","Feb"),("03","Mar"),("04","Apr"),("05","May"),("06","June"),("07","July"),("08","August"),("09","Sept"),("10","Oct"),("11","Nov"),("12","Dec")]
    choices3 = forms.ChoiceField(choices=month, label="Month")
    c4  = [("1","Uncategorized"),("2","Categorized"),("3","All")]
    choices4 = forms.ChoiceField(choices=c4, label="Type")

class CategorizeForm(forms.Form):
    categorize_choices = [("Uncategorized","Uncategorized"),("Expense","Expense"),("Employee Transfer","Employee Transfer"),("Salary","Salary"),("Sales","Sales"),("Refund","Refund"),("Sales Refund","Sales Refund"),("Other","Other")]
    categorize = forms.ChoiceField(choices=categorize_choices, widget=forms.RadioSelect)

class CategorizeEmployeeTransfer(forms.Form):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(),label="Receiver")


class ViewStatementForm(forms.Form):
    c  = [("1","Main"),("2","BIRAC")]
    choices = forms.ChoiceField(choices=c, label="Select Account Type")
    year =[(str(i),str(i)) for i in range(2017,datetime.datetime.now().year + 1)]
    choices2 = forms.ChoiceField(choices=year, label="Year")
    month = [("01","Jan"),("02","Feb"),("03","Mar"),("04","Apr"),("05","May"),("06","June"),("07","July"),("08","August"),("09","Sept"),("10","Oct"),("11","Nov"),("12","Dec")]
    choices3 = forms.ChoiceField(choices=month, label="Month")
    c4  = [("1","Uncategorized"),("2","Categorized"),("3","All")]
    choices4 = forms.ChoiceField(choices=c4, label="Type")

class MarkAccountForm(forms.Form):
    c  = [("1","Yes"),("2","No")]
    choices = forms.ChoiceField(choices=c, label="Are you Sure you want to mark Account?",widget=forms.RadioSelect)

class ViewMarkAccountForm(forms.Form):
    c_account  = [("1","Yes"),("2","No")]
    choices = forms.ChoiceField(choices=c_account, label="Are you Sure you want to mark Account?",widget=forms.RadioSelect)
class ViewMarkAuditForm(forms.Form):
    c_audit  = [("1","Yes"),("2","No")]
    choices = forms.ChoiceField(choices=c_audit, label="Are you Sure you want to mark Audited?",widget=forms.RadioSelect)
