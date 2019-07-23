from django.shortcuts import render,redirect
from django.http import HttpResponse
import csv, io
from django.contrib import messages
from .models import fm_txn,fm_utrans,fm_user_extend,fm_project,fm_budgethead,fm_ptcform,fm_ptctrans
from django.views.generic import TemplateView
import os.path
from .forms import AccountTypeForm,TransferMoneyForm,AddProjectForm,ProjectBudgetForm,ProjectBudgetForm2,ProjectBudgetForm3,ProjectBudgetForm4,ProjectBudgetForm5,ProjectBudgetForm6,ProjectBudgetForm7,ProjectBudgetForm8,ProjectBudgetForm9,ProjectBudgetForm10,ptcprojectform,ptctransform
from .forms import ptctransform2,ptctransform3,ptctransform4,ptctransform5,ptctransform6,ptctransform7,ptctransform8,ptctransform9,ptctransform10,ptctransform11,ptctransform12,ptctransform13,ptctransform14,ptctransform15
from .forms import CheckStatementForm,CategorizeForm,CategorizeEmployeeTransfer,ViewStatementForm,MarkAccountForm,ViewMarkAccountForm,ViewMarkAuditForm
from django.conf import settings
from django.db import IntegrityError
import uuid
import os.path
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from easy_pdf.views import PDFTemplateView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import AccessMixin
# Create your views here.
def account_type(request):
    return render(request,"account_type.html")

class AccountType(AccessMixin, TemplateView):
    template_name = "account_type.html"
    option_selected = ''
    accountID = 0
    # accountID = 0
    show_csv = 'No'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return redirect("/login/")
        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        if (("director" in [str(i) for i in request.user.groups.all()]) == True or (request.user.is_superuser == True)):
            form = AccountTypeForm()
            return render(request, self.template_name, {'form':form})
        else:
            user_access = 'No'
            return render(request, self.template_name, {'user_access':user_access})
    def post(self, request):
        show_csv = 'Yes'

        form = AccountTypeForm(request.POST)
        if form.is_valid():
            option_selected = form.cleaned_data['choices']
            option_selected = int(option_selected)
            global accountID
            accountID = option_selected
            # accountID = option_selected
            record  = fm_txn.objects.filter(accID=option_selected)
            message = ''
            obj = 0
            if record.count()==0:   #  count=0 i.e. no record present for particular account type
                # message = 'No record corresponding to this account type is present.'
                pass
            else:
                obj = record
                obj = obj.order_by('transc_time').reverse()
                obj = obj[:2]

            # 'form' for displayong 1st form,'obj' - if 0 display no previous records for particular accID,'show_csv'-for telling whether to show csv upload form or not

            return render(request, self.template_name,{'form':form,'obj':obj,'show_csv':show_csv})

        else:

            csv_file = request.FILES['file']
            error = False
            #Checking if file is of type CSV or not
            if not csv_file.name.endswith('.csv'):
                error = True
                # if error is True then selected file is not csv

            else:
                try:
                    name_diff_csv = uuid.uuid4().hex + '.csv'
                    complete_name = os.path.join("erpAPP/media/file_link/",name_diff_csv)

                    result = ''
                    duplicate = 0
                    imported = 0
                    balance_check = ''
                    field_object = 0.0


                    #Taking the dataset from csv file come through post request
                    data_set = csv_file.read().decode('UTF-8')

                    #loop through all data using streams
                    io_string = io.StringIO(data_set)

                    #Skipping first line of csv  as it contain headers
                    next(io_string)


                        #last used to check database integrity
                    last = fm_txn.objects.all()
                    last = last.order_by('transc_time').reverse()
                    balance_temp = 1
                    balance_check = 'unsuccess,file is not imported'
                    if last.exists():
                        last = last.first()
                        field_object = fm_txn.objects.filter(txnID=last).values('txnBalance').get()
                        field_object = field_object['txnBalance']


                    for column in csv.reader(io_string, delimiter=',',quotechar="|"):
                        if balance_temp == 1:
                            if column[8] == str(field_object) or field_object == 0.0:
                                # checking integrity check of balance
                                balance_check = True
                                balance_temp = 0
                            else:
                                balance_check = False
                                balance_temp = 0



                        if balance_check == True:
                            try:
                                dash, created = fm_txn.objects.update_or_create(
                                txnID = column[0],
                                accID = accountID,
                                txnDate = column[2],
                                txnPostedDate = column[3],
                                txnCheque = column[4],
                                txnDir = column[5],
                                txnDesc = column[6],
                                txnValue = column[7],
                                txnBalance = column[8],
                                txnAuditFile = name_diff_csv,

                                )
                                imported = imported + 1
                            except IntegrityError :      #IntegrityError - Error for primary key
                                result = 'unsuccess,file is not imported as same transaction exists already'
                                duplicate = duplicate + 1

                                    # total transaction = imported + duplicate



                    if imported>0:
                        result = 'success,file is imported'
                        file = open(complete_name,"w")
                        file.writelines(data_set)
                        file.close()
                    # path_csv = "/media/file_link/" + name_diff_csv
                    total_trnsactions = imported + duplicate

                    return render(request, "pmTransactionResult.html",{'balance_check':balance_check,'result':result,'imported':imported,'duplicate':duplicate,'total_trnsactions':total_trnsactions})
                except Exception as e:
                    return render(request, "pmTransactionResult.html",{'e':e})
            return render(request, "pmTransactionResult.html",{'error':error})
        return render(request,self.template_name)

def CompleteTransaction(request):
    untagged_objects = fm_txn.objects.filter(txnType='U')
    return render(request,'CompleteTransaction.html',{'untagged_objects':untagged_objects})


class transferMoney(AccessMixin, CreateView):
    model = fm_utrans
    template_name = 'transferMoney.html'
    fields = ['utranValue','utranDesc','utranReceiver']
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return redirect("/login/")
        if not (("director" in [str(i) for i in request.user.groups.all()]) == True or (request.user.is_superuser == True) or ("projectmanager" in [str(i) for i in request.user.groups.all()]) == True):
            # Redirect the user to somewhere else - add your URL here
            user_access = 'No'
            return render(request,"transferMoney.html",{"user_access":user_access})

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        form.instance.utranSender = self.request.user.id
        return super(transferMoney, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('transferMoneysuccess')

@login_required(login_url = "/login/")
def transferMoneysuccess(request):
    return render(request, "transferMoneysuccess.html")
@login_required(login_url = "/login/")
def financialAccount(request):
    record = fm_utrans.objects.filter(utranReceiver=request.user.id)
    record = record.filter(utranConfirmed='N')
    record_message = record.exists()
    overview = fm_user_extend.objects.filter(user=request.user.id)
    record_confirmed = fm_utrans.objects.filter(utranConfirmed='Y')
    record_confirmed_Cr = record_confirmed.filter(utranReceiver=request.user.id)
    record_confirmed_Dr = record_confirmed.filter(utranSender=request.user.id)
    if record_confirmed_Cr.exists()==False and record_confirmed_Dr.exists()==False:
        record_confirmed_message = False
    else:
        record_confirmed_message = True
    return render(request,"financialAccount.html",{'record':record,'record_confirmed_Cr':record_confirmed_Cr,'record_confirmed_Dr':record_confirmed_Dr,'record_message':record_message,'record_confirmed_message':record_confirmed_message,'overview':overview})
@login_required(login_url = "/login/")
def accept(request,pk):
    record = fm_utrans.objects.get(id=pk)
    record.utranConfirmed = 'Y'
    record.save()
    return render(request,"accept.html")
@login_required(login_url = "/login/")
def decline(request,pk):
    record = fm_utrans.objects.get(id=pk)
    record.utranConfirmed = 'D'
    record.save()
    return render(request,"decline.html")

class addproject(AccessMixin, TemplateView):
    template_name = "add_project.html"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return redirect("/login/")
        if not (request.user.is_superuser == True):
            # Redirect the user to somewhere else - add your URL here
            user_access = 'No'
            return render(request,"add_project.html",{"user_access":user_access})

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        form = AddProjectForm()
        form2 = ProjectBudgetForm()
        form3 = ProjectBudgetForm2()
        form4 = ProjectBudgetForm3()
        form5 = ProjectBudgetForm4()
        form6 = ProjectBudgetForm5()
        form7 = ProjectBudgetForm6()
        form8 = ProjectBudgetForm7()
        form9 = ProjectBudgetForm8()
        form10 = ProjectBudgetForm9()
        form11 = ProjectBudgetForm10()
        return render(request,self.template_name,{'form':form,'form2':form2,'form3':form3,'form4':form4,'form5':form5,'form6':form6,'form7':form7,'form8':form8,'form9':form9,'form10':form10,'form11':form11})
    def post(self,request):
        error = 0
        form = AddProjectForm(request.POST)
        form2 = ProjectBudgetForm(request.POST)
        form3 = ProjectBudgetForm2(request.POST)
        form4 = ProjectBudgetForm3(request.POST)
        form5 = ProjectBudgetForm4(request.POST)
        form6 = ProjectBudgetForm5(request.POST)
        form7 = ProjectBudgetForm6(request.POST)
        form8 = ProjectBudgetForm7(request.POST)
        form9 = ProjectBudgetForm8(request.POST)
        form10 = ProjectBudgetForm9(request.POST)
        form11 = ProjectBudgetForm10(request.POST)
        try:
            title_check = fm_project.objects.filter(prTitle = request.POST.get("prTitle"))
            if not title_check:
                if form.is_valid():
                    if form2.is_valid():
                        form.save()
                        obj = fm_project.objects.latest('id')
                        new_req = fm_budgethead(prID=obj,bhTitle=request.POST['title'],bhLimit=request.POST['Limit'],bhBalance=request.POST['Balance'])
                        new_req.save()
                    if (form3.is_valid() and form4.is_valid() and form5.is_valid() and form6.is_valid() and form7.is_valid() and form8.is_valid() and form9.is_valid() and form10.is_valid() and form11.is_valid()):
                        for i in range(2,11):
                                if not (request.POST['title'+str(i)]==""):
                                    if request.POST['Limit'+str(i)]=='':
                                        if request.POST['Balance'+str(i)]=='':
                                            new_req = fm_budgethead(prID=obj,bhTitle=request.POST['title'+str(i)],bhLimit=0,bhBalance=0)
                                            new_req.save()
                                        else:
                                            new_req = fm_budgethead(prID=obj,bhTitle=request.POST['title'+str(i)],bhLimit=0,bhBalance=request.POST['Balance'+str(i)])
                                            new_req.save()
                                    elif request.POST['Balance'+str(i)]=='':
                                        if not (request.POST['Limit'+str(i)]==''):
                                            new_req = fm_budgethead(prID=obj,bhTitle=request.POST['title'+str(i)],bhLimit=request.POST['Limit'+str(i)],bhBalance=0)
                                            new_req.save()
                                    else:
                                        new_req = fm_budgethead(prID=obj,bhTitle=request.POST['title'+str(i)],bhLimit=request.POST['Limit'+str(i)],bhBalance=request.POST['Balance'+str(i)])
                                        new_req.save()


                    else:
                        error = 1
            else:
                error=1
                message="This project title already exists"
        except Exception as e:
            message = e
        if error==1:
            return render(request,self.template_name,{'error':error,'message':message})
        else:
            obj = fm_project.objects.latest('id')
            budget = fm_budgethead.objects.filter(prID=obj)
            return render(request,"add_project_success.html",{'obj':obj,'budget':budget})

        return render(request,self.template_name)

class ProjectSuccessPDFView(PDFTemplateView):
    template_name = 'add_project_success_pdf.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = fm_project.objects.latest('id')
        context['budget'] = fm_budgethead.objects.filter(prID=fm_project.objects.latest('id'))
        return context

def ptcproject(request):
    if request.method=="GET":
        form = ptcprojectform()
        return render(request,"ptcproject.html",{'form':form})

    if request.method == "POST":
        form = ptcprojectform(request.POST)
        name = request.POST.get("ptcprojectform")
        name2 = request.POST.get("ptctransform")
        budget_id = request.POST.get("prID")
        if (name == "Submit" and name2==None):
            budget_queryset = fm_budgethead.objects.filter(prID = budget_id)
            form_trans = ptctransform(budget_queryset)
            form_trans2 = ptctransform2(budget_queryset)
            form_trans3 = ptctransform3(budget_queryset)
            form_trans4 = ptctransform4(budget_queryset)
            form_trans5 = ptctransform5(budget_queryset)
            form_trans6 = ptctransform6(budget_queryset)
            form_trans7 = ptctransform7(budget_queryset)
            form_trans8 = ptctransform8(budget_queryset)
            form_trans9 = ptctransform9(budget_queryset)
            form_trans10 = ptctransform10(budget_queryset)
            form_trans11 = ptctransform11(budget_queryset)
            form_trans12 = ptctransform12(budget_queryset)
            form_trans13 = ptctransform13(budget_queryset)
            form_trans14 = ptctransform14(budget_queryset)
            form_trans15 = ptctransform15(budget_queryset)
            return render(request,"ptcproject.html",{'form_trans':form_trans,'form_trans2':form_trans2,'form_trans3':form_trans3,'form_trans4':form_trans4,'form_trans5':form_trans5,'form_trans6':form_trans6,'form_trans7':form_trans7,'form_trans8':form_trans8,'form_trans9':form_trans9,'form_trans10':form_trans10,'form_trans11':form_trans11,'form_trans12':form_trans12,'form_trans13':form_trans13,'form_trans14':form_trans14,'form_trans15':form_trans15})
        if (name2=="Submit" and name==None):
            budget_obj = fm_budgethead.objects.filter(id = request.POST['Budgets']).values('prID')
            for i in budget_obj:
                pr_id = i['prID']
                break
            pr_obj = fm_project.objects.filter(id=pr_id)
            for i in pr_obj:
                pr_obj = i
                break
            for j in User.objects.filter(id = request.user.id):
                user_obj = j
                break
            budget_form_obj = fm_budgethead.objects.filter(id = request.POST['Budgets'])
            for k in budget_form_obj:
                budget_form_obj = k
                break
            if request.POST['Budgets']:
                budget_form_obj = fm_budgethead.objects.filter(id = request.POST['Budgets'])
                for k in budget_form_obj:
                    budget_form_obj = k
                    break
            if request.POST['Budgets2']:
                budget_form_obj2 = fm_budgethead.objects.filter(id = request.POST['Budgets2'])
                for k in budget_form_obj2:
                    budget_form_obj2 = k
                    break
            if request.POST['Budgets3']:
                budget_form_obj3 = fm_budgethead.objects.filter(id = request.POST['Budgets3'])
                for k in budget_form_obj3:
                    budget_form_obj3 = k
                    break
            if request.POST['Budgets3']:
                budget_form_obj3 = fm_budgethead.objects.filter(id = request.POST['Budgets3'])
                for k in budget_form_obj3:
                    budget_form_obj3 = k
                    break
            if request.POST['Budgets4']:
                budget_form_obj4 = fm_budgethead.objects.filter(id = request.POST['Budgets4'])
                for k in budget_form_obj4:
                    budget_form_obj4 = k
                    break
            if request.POST['Budgets5']:
                budget_form_obj5 = fm_budgethead.objects.filter(id = request.POST['Budgets5'])
                for k in budget_form_obj5:
                    budget_form_obj5 = k
                    break
            if request.POST['Budgets6']:
                budget_form_obj6 = fm_budgethead.objects.filter(id = request.POST['Budgets6'])
                for k in budget_form_obj6:
                    budget_form_obj6 = k
                    break
            if request.POST['Budgets7']:
                budget_form_obj7 = fm_budgethead.objects.filter(id = request.POST['Budgets7'])
                for k in budget_form_obj7:
                    budget_form_obj7 = k
                    break
            if request.POST['Budgets8']:
                budget_form_obj8 = fm_budgethead.objects.filter(id = request.POST['Budgets8'])
                for k in budget_form_obj8:
                    budget_form_obj8 = k
                    break
            if request.POST['Budgets9']:
                budget_form_obj9 = fm_budgethead.objects.filter(id = request.POST['Budgets9'])
                for k in budget_form_obj9:
                    budget_form_obj9 = k
                    break
            if request.POST['Budgets10']:
                budget_form_obj10 = fm_budgethead.objects.filter(id = request.POST['Budgets10'])
                for k in budget_form_obj10:
                    budget_form_obj10 = k
                    break
            if request.POST['Budgets11']:
                budget_form_obj11 = fm_budgethead.objects.filter(id = request.POST['Budgets11'])
                for k in budget_form_obj11:
                    budget_form_obj11 = k
                    break
            if request.POST['Budgets12']:
                budget_form_obj12 = fm_budgethead.objects.filter(id = request.POST['Budgets12'])
                for k in budget_form_obj12:
                    budget_form_obj12 = k
                    break
            if request.POST['Budgets13']:
                budget_form_obj13 = fm_budgethead.objects.filter(id = request.POST['Budgets13'])
                for k in budget_form_obj13:
                    budget_form_obj13 = k
                    break
            if request.POST['Budgets14']:
                budget_form_obj14 = fm_budgethead.objects.filter(id = request.POST['Budgets14'])
                for k in budget_form_obj14:
                    budget_form_obj14 = k
                    break
            if request.POST['Budgets15']:
                budget_form_obj15 = fm_budgethead.objects.filter(id = request.POST['Budgets15'])
                for k in budget_form_obj15:
                    budget_form_obj15 = k
                    break
            try:
                new_req = fm_ptctrans(ptctransDate = request.POST['Date_ptcform'],ptcVendor=request.POST['Vendor'],ptcDesc=request.POST['Description'],ptctransValue=request.POST['Value'],ptctransHead=budget_form_obj,ptctransInvoiceStatus =request.POST['choices'], ptctransInvoiceFile=request.FILES['file'])
                if not (request.POST['Date_ptcform2']== "" or request.POST['Vendor2']=="" or request.POST['Description2']=="" or request.POST['Value2']=="" or request.POST['choices2']=="" or request.FILES['file2']=="" or request.POST['Budgets2']==""):
                    new_req2 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform2'],ptcVendor=request.POST['Vendor2'],ptcDesc=request.POST['Description2'],ptctransValue=request.POST['Value2'],ptctransHead=budget_form_obj2,ptctransInvoiceStatus =request.POST['choices2'], ptctransInvoiceFile=request.FILES['file2'])
                if not (request.POST['Date_ptcform3']== "" or request.POST['Vendor3']=="" or request.POST['Description3']=="" or request.POST['Value3']=="" or request.POST['choices3']=="" or request.FILES['file3']=="" or request.POST['Budgets3']==""):
                    new_req3 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform3'],ptcVendor=request.POST['Vendor3'],ptcDesc=request.POST['Description3'],ptctransValue=request.POST['Value3'],ptctransHead=budget_form_obj3,ptctransInvoiceStatus =request.POST['choices3'], ptctransInvoiceFile=request.FILES['file3'])
                if not (request.POST['Date_ptcform4']== "" or request.POST['Vendor4']=="" or request.POST['Description4']=="" or request.POST['Value4']=="" or request.POST['choices4']=="" or request.FILES['file4']=="" or request.POST['Budgets4']==""):
                    new_req4 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform4'],ptcVendor=request.POST['Vendor4'],ptcDesc=request.POST['Description4'],ptctransValue=request.POST['Value4'],ptctransHead=budget_form_obj4,ptctransInvoiceStatus =request.POST['choices4'], ptctransInvoiceFile=request.FILES['file4'])
                if not (request.POST['Date_ptcform5']== "" or request.POST['Vendor5']=="" or request.POST['Description5']=="" or request.POST['Value5']=="" or request.POST['choices5']=="" or request.FILES['file5']=="" or request.POST['Budgets5']==""):
                    new_req5 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform5'],ptcVendor=request.POST['Vendor5'],ptcDesc=request.POST['Description5'],ptctransValue=request.POST['Value5'],ptctransHead=budget_form_obj5,ptctransInvoiceStatus =request.POST['choices5'], ptctransInvoiceFile=request.FILES['file5'])
                if not (request.POST['Date_ptcform6']== "" or request.POST['Vendor6']=="" or request.POST['Description6']=="" or request.POST['Value6']=="" or request.POST['choices6']=="" or request.FILES['file6']=="" or request.POST['Budgets6']==""):
                    new_req6 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform6'],ptcVendor=request.POST['Vendor6'],ptcDesc=request.POST['Description6'],ptctransValue=request.POST['Value6'],ptctransHead=budget_form_obj6,ptctransInvoiceStatus =request.POST['choices6'], ptctransInvoiceFile=request.FILES['file6'])
                if not (request.POST['Date_ptcform7']== "" or request.POST['Vendor7']=="" or request.POST['Description7']=="" or request.POST['Value7']=="" or request.POST['choices7']=="" or request.FILES['file7']=="" or request.POST['Budgets7']==""):
                    new_req7 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform7'],ptcVendor=request.POST['Vendor7'],ptcDesc=request.POST['Description7'],ptctransValue=request.POST['Value7'],ptctransHead=budget_form_obj7,ptctransInvoiceStatus =request.POST['choices7'], ptctransInvoiceFile=request.FILES['file7'])
                if not (request.POST['Date_ptcform8']== "" or request.POST['Vendor8']=="" or request.POST['Description8']=="" or request.POST['Value8']=="" or request.POST['choices8']=="" or request.FILES['file8']=="" or request.POST['Budgets8']==""):
                    new_req8 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform8'],ptcVendor=request.POST['Vendor8'],ptcDesc=request.POST['Description8'],ptctransValue=request.POST['Value8'],ptctransHead=budget_form_obj8,ptctransInvoiceStatus =request.POST['choices8'], ptctransInvoiceFile=request.FILES['file8'])
                if not (request.POST['Date_ptcform9']== "" or request.POST['Vendor9']=="" or request.POST['Description9']=="" or request.POST['Value9']=="" or request.POST['choices9']=="" or request.FILES['file9']=="" or request.POST['Budgets9']==""):
                    new_req9 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform9'],ptcVendor=request.POST['Vendor9'],ptcDesc=request.POST['Description9'],ptctransValue=request.POST['Value9'],ptctransHead=budget_form_obj9,ptctransInvoiceStatus =request.POST['choices9'], ptctransInvoiceFile=request.FILES['file9'])
                if not (request.POST['Date_ptcform10']== "" or request.POST['Vendor10']=="" or request.POST['Description10']=="" or request.POST['Value10']=="" or request.POST['choices10']=="" or request.FILES['file10']=="" or request.POST['Budgets10']==""):
                    new_req10 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform10'],ptcVendor=request.POST['Vendor10'],ptcDesc=request.POST['Description10'],ptctransValue=request.POST['Value10'],ptctransHead=budget_form_obj10,ptctransInvoiceStatus =request.POST['choices10'], ptctransInvoiceFile=request.FILES['file10'])
                if not (request.POST['Date_ptcform11']== "" or request.POST['Vendor11']=="" or request.POST['Description11']=="" or request.POST['Value11']=="" or request.POST['choices11']=="" or request.FILES['file11']=="" or request.POST['Budgets11']==""):
                    new_req11 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform11'],ptcVendor=request.POST['Vendor11'],ptcDesc=request.POST['Description11'],ptctransValue=request.POST['Value11'],ptctransHead=budget_form_obj11,ptctransInvoiceStatus =request.POST['choices11'], ptctransInvoiceFile=request.FILES['file11'])
                if not (request.POST['Date_ptcform12']== "" or request.POST['Vendor12']=="" or request.POST['Description12']=="" or request.POST['Value12']=="" or request.POST['choices12']=="" or request.FILES['file12']=="" or request.POST['Budgets12']==""):
                    new_req12 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform12'],ptcVendor=request.POST['Vendor12'],ptcDesc=request.POST['Description12'],ptctransValue=request.POST['Value12'],ptctransHead=budget_form_obj12,ptctransInvoiceStatus =request.POST['choices12'], ptctransInvoiceFile=request.FILES['file12'])
                if not (request.POST['Date_ptcform13']== "" or request.POST['Vendor13']=="" or request.POST['Description13']=="" or request.POST['Value13']=="" or request.POST['choices13']=="" or request.FILES['file13']=="" or request.POST['Budgets13']==""):
                    new_req13 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform13'],ptcVendor=request.POST['Vendor13'],ptcDesc=request.POST['Description13'],ptctransValue=request.POST['Value13'],ptctransHead=budget_form_obj13,ptctransInvoiceStatus =request.POST['choices13'], ptctransInvoiceFile=request.FILES['file13'])
                if not (request.POST['Date_ptcform14']== "" or request.POST['Vendor14']=="" or request.POST['Description14']=="" or request.POST['Value14']=="" or request.POST['choices14']=="" or request.FILES['file14']=="" or request.POST['Budgets14']==""):
                    new_req14 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform14'],ptcVendor=request.POST['Vendor14'],ptcDesc=request.POST['Description14'],ptctransValue=request.POST['Value14'],ptctransHead=budget_form_obj14,ptctransInvoiceStatus =request.POST['choices14'], ptctransInvoiceFile=request.FILES['file14'])
                if not (request.POST['Date_ptcform15']== "" or request.POST['Vendor15']=="" or request.POST['Description15']=="" or request.POST['Value15']=="" or request.POST['choices15']=="" or request.FILES['file15']=="" or request.POST['Budgets15']==""):
                    new_req15 = fm_ptctrans(ptctransDate = request.POST['Date_ptcform15'],ptcVendor=request.POST['Vendor15'],ptcDesc=request.POST['Description15'],ptctransValue=request.POST['Value15'],ptctransHead=budget_form_obj15,ptctransInvoiceStatus =request.POST['choices15'], ptctransInvoiceFile=request.FILES['file15'])



            except Exception as e :
                return render(request,"ptcproject.html",{'e':e})
            fm_ptcform.objects.create(uID=j,prID=pr_obj)
            ptc_obj = fm_ptcform.objects.latest()
            try:
                new_req = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform'],ptcVendor=request.POST['Vendor'],ptcDesc=request.POST['Description'],ptctransValue=request.POST['Value'],ptctransHead=budget_form_obj,ptctransInvoiceStatus =request.POST['choices'], ptctransInvoiceFile=request.FILES['file'])
                new_req.save()
                if not (request.POST['Date_ptcform2']== "" or request.POST['Vendor2']=="" or request.POST['Description2']=="" or request.POST['Value2']=="" or request.POST['choices2']=="" or request.FILES['file2']=="" or request.POST['Budgets2']=="=="""):
                    new_req2 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform2'],ptcVendor=request.POST['Vendor2'],ptcDesc=request.POST['Description2'],ptctransValue=request.POST['Value2'],ptctransHead=budget_form_obj2,ptctransInvoiceStatus =request.POST['choices2'], ptctransInvoiceFile=request.FILES['file2'])
                    new_req2.save()
                if not (request.POST['Date_ptcform3']== "" or request.POST['Vendor3']=="" or request.POST['Description3']=="" or request.POST['Value3']=="" or request.POST['choices3']=="" or request.FILES['file3']=="" or request.POST['Budgets3']==""):
                    new_req3 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform3'],ptcVendor=request.POST['Vendor3'],ptcDesc=request.POST['Description3'],ptctransValue=request.POST['Value3'],ptctransHead=budget_form_obj3,ptctransInvoiceStatus =request.POST['choices3'], ptctransInvoiceFile=request.FILES['file3'])
                    new_req3.save()
                if not (request.POST['Date_ptcform4']== "" or request.POST['Vendor4']=="" or request.POST['Description4']=="" or request.POST['Value4']=="" or request.POST['choices4']=="" or request.FILES['file4']=="" or request.POST['Budgets4']==""):
                    new_req4 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform4'],ptcVendor=request.POST['Vendor4'],ptcDesc=request.POST['Description4'],ptctransValue=request.POST['Value4'],ptctransHead=budget_form_obj4,ptctransInvoiceStatus =request.POST['choices4'], ptctransInvoiceFile=request.FILES['file4'])
                    new_req4.save()
                if not (request.POST['Date_ptcform5']== "" or request.POST['Vendor5']=="" or request.POST['Description5']=="" or request.POST['Value5']=="" or request.POST['choices5']=="" or request.FILES['file5']=="" or request.POST['Budgets5']==""):
                    new_req5 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform5'],ptcVendor=request.POST['Vendor5'],ptcDesc=request.POST['Description5'],ptctransValue=request.POST['Value5'],ptctransHead=budget_form_obj5,ptctransInvoiceStatus =request.POST['choices5'], ptctransInvoiceFile=request.FILES['file5'])
                    new_req5.save()
                if not (request.POST['Date_ptcform6']== "" or request.POST['Vendor6']=="" or request.POST['Description6']=="" or request.POST['Value6']=="" or request.POST['choices6']=="" or request.FILES['file6']=="" or request.POST['Budgets6']==""):
                    new_req6 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform6'],ptcVendor=request.POST['Vendor6'],ptcDesc=request.POST['Description6'],ptctransValue=request.POST['Value6'],ptctransHead=budget_form_obj6,ptctransInvoiceStatus =request.POST['choices6'], ptctransInvoiceFile=request.FILES['file6'])
                    new_req6.save()
                if not (request.POST['Date_ptcform7']== "" or request.POST['Vendor7']=="" or request.POST['Description7']=="" or request.POST['Value7']=="" or request.POST['choices7']=="" or request.FILES['file7']=="" or request.POST['Budgets7']==""):
                    new_req7 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform7'],ptcVendor=request.POST['Vendor7'],ptcDesc=request.POST['Description7'],ptctransValue=request.POST['Value7'],ptctransHead=budget_form_obj7,ptctransInvoiceStatus =request.POST['choices7'], ptctransInvoiceFile=request.FILES['file7'])
                    new_req7.save()
                if not (request.POST['Date_ptcform8']== "" or request.POST['Vendor8']=="" or request.POST['Description8']=="" or request.POST['Value8']=="" or request.POST['choices8']=="" or request.FILES['file8']=="" or request.POST['Budgets8']==""):
                    new_req8 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform8'],ptcVendor=request.POST['Vendor8'],ptcDesc=request.POST['Description8'],ptctransValue=request.POST['Value8'],ptctransHead=budget_form_obj8,ptctransInvoiceStatus =request.POST['choices8'], ptctransInvoiceFile=request.FILES['file8'])
                    new_req8.save()
                if not (request.POST['Date_ptcform9']== "" or request.POST['Vendor9']=="" or request.POST['Description9']=="" or request.POST['Value9']=="" or request.POST['choices9']=="" or request.FILES['file9']=="" or request.POST['Budgets9']==""):
                    new_req9 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform9'],ptcVendor=request.POST['Vendor9'],ptcDesc=request.POST['Description9'],ptctransValue=request.POST['Value9'],ptctransHead=budget_form_obj9,ptctransInvoiceStatus =request.POST['choices9'], ptctransInvoiceFile=request.FILES['file9'])
                    new_req9.save()
                if not (request.POST['Date_ptcform10']== "" or request.POST['Vendor10']=="" or request.POST['Description10']=="" or request.POST['Value10']=="" or request.POST['choices10']=="" or request.FILES['file10']=="" or request.POST['Budgets10']==""):
                    new_req10 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform10'],ptcVendor=request.POST['Vendor10'],ptcDesc=request.POST['Description10'],ptctransValue=request.POST['Value10'],ptctransHead=budget_form_obj10,ptctransInvoiceStatus =request.POST['choices10'], ptctransInvoiceFile=request.FILES['file10'])
                    new_req10.save()
                if not (request.POST['Date_ptcform11']== "" or request.POST['Vendor11']=="" or request.POST['Description11']=="" or request.POST['Value11']=="" or request.POST['choices11']=="" or request.FILES['file11']=="" or request.POST['Budgets11']==""):
                    new_req11 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform11'],ptcVendor=request.POST['Vendor11'],ptcDesc=request.POST['Description11'],ptctransValue=request.POST['Value11'],ptctransHead=budget_form_obj11,ptctransInvoiceStatus =request.POST['choices11'], ptctransInvoiceFile=request.FILES['file11'])
                    new_req11.save()
                if not (request.POST['Date_ptcform12']== "" or request.POST['Vendor12']=="" or request.POST['Description12']=="" or request.POST['Value12']=="" or request.POST['choices12']=="" or request.FILES['file12']=="" or request.POST['Budgets12']==""):
                    new_req12 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform12'],ptcVendor=request.POST['Vendor12'],ptcDesc=request.POST['Description12'],ptctransValue=request.POST['Value12'],ptctransHead=budget_form_obj12,ptctransInvoiceStatus =request.POST['choices12'], ptctransInvoiceFile=request.FILES['file12'])
                    new_req12.save()
                if not (request.POST['Date_ptcform13']== "" or request.POST['Vendor13']=="" or request.POST['Description13']=="" or request.POST['Value13']=="" or request.POST['choices13']=="" or request.FILES['file13']=="" or request.POST['Budgets13']==""):
                    new_req13 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform13'],ptcVendor=request.POST['Vendor13'],ptcDesc=request.POST['Description13'],ptctransValue=request.POST['Value13'],ptctransHead=budget_form_obj13,ptctransInvoiceStatus =request.POST['choices13'], ptctransInvoiceFile=request.FILES['file13'])
                    new_req13.save()
                if not (request.POST['Date_ptcform14']== "" or request.POST['Vendor14']=="" or request.POST['Description14']=="" or request.POST['Value14']=="" or request.POST['choices14']=="" or request.FILES['file14']=="" or request.POST['Budgets14']==""):
                    new_req14 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform14'],ptcVendor=request.POST['Vendor14'],ptcDesc=request.POST['Description14'],ptctransValue=request.POST['Value14'],ptctransHead=budget_form_obj14,ptctransInvoiceStatus =request.POST['choices14'], ptctransInvoiceFile=request.FILES['file14'])
                    new_req14.save()
                if not (request.POST['Date_ptcform15']== "" or request.POST['Vendor15']=="" or request.POST['Description15']=="" or request.POST['Value15']=="" or request.POST['choices15']=="" or request.FILES['file15']=="" or request.POST['Budgets15']==""):
                    new_req15 = fm_ptctrans(uID=j,prID=pr_obj,ptcID=ptc_obj,ptctransDate = request.POST['Date_ptcform15'],ptcVendor=request.POST['Vendor15'],ptcDesc=request.POST['Description15'],ptctransValue=request.POST['Value15'],ptctransHead=budget_form_obj15,ptctransInvoiceStatus =request.POST['choices15'], ptctransInvoiceFile=request.FILES['file15'])
                    new_req15.save()

            except Exception as e:
                return render(request,"ptcproject.html",{'e':e})
            sum = int(request.POST['Value'])
            for m in range(2,16):
                if not request.POST['Value' + str(m)] == "":
                    sum = sum + int(request.POST['Value' + str(m)])
            ptc_obj.ptcValue = sum
            ptc_obj.save()
            ptctrans_obj = fm_ptctrans.objects.filter(ptcID=ptc_obj)
            li=[]
            for i in ptctrans_obj:
                a = getattr(i, "ptctransHead")
                a = getattr(a, "bhTitle")
                b = getattr(i, "ptctransValue")
                li.append([a,b])
            show_result = 'Yes'
            ##process petty cash form after submitting ptctrans form
    return render(request,"ptcproject.html",{'li':li,'sum':sum,'show_result':show_result})

def CheckStatement(request):
    if request.method=="GET":
        form = CheckStatementForm()
        return render(request,"CheckStatement.html",{"form":form})
    if request.method=="POST":
        form = CheckStatementForm(request.POST)
        name = request.POST.get("checkstatementform")
        if form.is_valid():
            if name=="Submit":
                if request.POST["choices4"] == "1": # uncategorized
                    obj = fm_txn.objects.filter(accID=request.POST["choices"]).filter(txnType = 'U').filter(txnDate__year=request.POST["choices2"]).filter(txnDate__month=request.POST["choices3"])
                elif request.POST["choices4"] == "2": # categorized
                    obj = fm_txn.objects.filter(accID=request.POST["choices"]).exclude(txnType = 'U').filter(txnDate__year=request.POST["choices2"]).filter(txnDate__month=request.POST["choices3"])
                elif request.POST["choices4"] == "3": # All
                    obj = fm_txn.objects.filter(accID=request.POST["choices"]).filter(txnDate__year=request.POST["choices2"]).filter(txnDate__month=request.POST["choices3"])
                if not obj:
                    message = "No record found for this."
                    return render(request,"CheckStatement.html",{"message":message})
                else:
                    return render(request,"CheckStatement.html",{'obj':obj})
        else:
            error = "Please check the details submitted"
            return render(request,"CheckStatement.html",{"error":error})
    return render(request,"CheckStatement.html")

def Categorize(request,txnID):
    if request.method=="GET":
        form = CategorizeForm()
        obj = fm_txn.objects.filter(txnID=txnID)
        return render(request,"categorize.html",{"form":form,"obj":obj})
    if request.method=="POST":
        form = CategorizeForm(request.POST)
        name = request.POST.get("EmployeeTransferForm")
        if form.is_valid():
            obj = fm_txn.objects.filter(txnID=txnID)
            for i in obj:
                obj = i
                break
            if request.POST['categorize'] == "Uncategorized":
                obj.txnType = "U"
                obj.save()
                success = "Uncategorized is updated"
                return render(request,"categorize.html",{"success":success})

            if request.POST['categorize'] == "Salary":
                obj.txnType = "S"
                obj.save()
                success = "Salary is Updated"
                return render(request,"categorize.html",{"success":success})
            if request.POST['categorize'] == "Expense":
                txnid_null = fm_ptcform.objects.filter(txnID=None)
                categorize = "expense"
                return render(request,"categorize.html",{"txnid_null":txnid_null,"categorize":categorize,"txnID":txnID})
            if request.POST['categorize'] == "Employee Transfer":
                txnid_null = fm_ptcform.objects.filter(txnID=None)
                categorize = "employee transfer"
                form = CategorizeEmployeeTransfer()
                return render(request,"categorize.html",{"txnid_null":txnid_null,"categorize":categorize,"txnID":txnID,"form":form})
        elif name == "Submit":
            form = CategorizeEmployeeTransfer(request.POST)
            obj = fm_txn.objects.filter(txnID=txnID)
            for i in obj:
                obj = i
                break
            try:
                user_obj = User.objects.filter(id = request.POST["receiver"])
                for i in user_obj:
                    user_obj = i
                    break
                print(user_obj)
                fm_utrans.objects.create(txnID=txnID,utranDesc=obj.txnDesc,utranValue=obj.txnValue,utranConfirmed='Y',utranSender=request.user.id,utranReceiver=user_obj)
                obj.txnType = 'T'
                obj.save()
                success = "Successfully Done"
                return render(request,"categorize.html",{"success":success})
            except Exception as e:
                error = e
                return render(request,"categorize.html",{"error":error})

        else:
            error = "Invalid Details"

    return render(request,"categorize.html",{"error":error})

def CategorizeExpense(request,txnID,pk):
    e = None
    try:

        ptc_form_obj = fm_ptcform.objects.filter(id=pk)
        txn_obj = fm_txn.objects.filter(txnID=txnID)
        for i in ptc_form_obj:
            ptc_form_obj = i
            break
        for i in txn_obj:
            txn_obj = i
            break
        ptc_form_obj.txnID = txn_obj
        ptc_form_obj.save()
        txn_obj.ptcID = pk
        txn_obj.txnType = "E"
        txn_obj.save()
    except Exception as e:
        pass
    return render(request,"categorizeExpense.html",{"e":e})

def ViewStatement(request):
    if request.method=="GET":
        form = ViewStatementForm()
        return render(request,"ViewStatement.html",{"form":form})
    if request.method=="POST":
        form = ViewStatementForm(request.POST)
        name = request.POST.get("viewstatementform")
        if form.is_valid():
            if name=="Submit":
                if request.POST["choices4"] == "1": # uncategorized
                    obj = fm_txn.objects.filter(accID=request.POST["choices"]).filter(txnType = 'U').filter(txnDate__year=request.POST["choices2"]).filter(txnDate__month=request.POST["choices3"])
                elif request.POST["choices4"] == "2": # categorized
                    obj = fm_txn.objects.filter(accID=request.POST["choices"]).exclude(txnType = 'U').filter(txnDate__year=request.POST["choices2"]).filter(txnDate__month=request.POST["choices3"])
                elif request.POST["choices4"] == "3": # All
                    obj = fm_txn.objects.filter(accID=request.POST["choices"]).filter(txnDate__year=request.POST["choices2"]).filter(txnDate__month=request.POST["choices3"])
                if not obj:
                    message = "No record found for this."
                    return render(request,"ViewStatement.html",{"message":message})
                else:
                    return render(request,"ViewStatement.html",{'obj':obj})
        else:
            error = "Please check the details submitted"

    return render(request,"ViewStatement.html",{"error":error})

def MarkAccount(request,txnID):
    if request.method=="GET":
        form = MarkAccountForm()
        return render(request,"MarkAccount.html",{'form':form})
    if request.method=="POST":
        form = MarkAccountForm(request.POST)
        if form.is_valid():
            name = request.POST.get("markaccountform")
            option = request.POST.get("choices")
            if name == "Submit" and option == "1":
                success = "Account Marked Succesfully"
                obj = fm_txn.objects.filter(txnID=txnID)

                for i in obj:
                    obj = i
                    break
                obj.txnAccounted = 1
                obj.save()
                return render(request,"MarkAccount.html",{'success':success})
            elif name == "Submit" and option == "2":
                success = 'Marking the Account is cancelled'
                obj = fm_txn.objects.filter(txnID=txnID)

                for i in obj:
                    obj = i
                    break
                obj.txnAccounted = 0
                obj.save()
                return render(request,"MarkAccount.html",{'success':success})
            else:
                error = "there is some error while processing input given."
        else:
            error = "Invalid Input Found"
    return render(request,"MarkAccount.html",{'error':error})

def ExpenseList(request,ptcID):
    try:
        ptc_obj = fm_ptcform.objects.filter(id=ptcID)
        obj = fm_ptctrans.objects.filter(ptcID = ptc_obj[0])
        return render(request,"ExpenseList.html",{'obj':obj})
    except:
        error = 'No petty cash form corresponding to this ID'
    return render(request,"ExpenseList.html",{'error':error})

def ViewMarkAccount(request,id):
    if request.method=="GET":
        form = ViewMarkAccountForm()
        return render(request,"ViewMarkAccount.html",{'form':form})
    if request.method=="POST":
        form = ViewMarkAccountForm(request.POST)
        if form.is_valid():
            name = request.POST.get("viewmarkaccountform")
            option = request.POST.get("choices")
            if name == "Submit" and option == "1":
                success = "Account Marked Succesfully"
                obj = fm_ptctrans.objects.filter(id=id)

                for i in obj:
                    obj = i
                    break
                obj.ptcAccounted = 1
                obj.save()
                return render(request,"ViewMarkAccount.html",{'success':success})
            elif name == "Submit" and option == "2":
                success = 'Marking the Account is cancelled'
                obj = fm_ptctrans.objects.filter(id=id)

                for i in obj:
                    obj = i
                    break
                obj.ptcAccounted = 0
                obj.save()
                return render(request,"ViewMarkAccount.html",{'success':success})
            else:
                error = "there is some error while processing input given."
        else:
            error = "Invalid Input Found"
    return render(request,"ViewMarkAccount.html",{'error':error})

def ViewMarkAudit(request,id):
    if request.method=="GET":
        form = ViewMarkAuditForm()
        return render(request,"ViewMarkAudit.html",{'form':form})
    if request.method=="POST":
        form = ViewMarkAuditForm(request.POST)
        if form.is_valid():
            name = request.POST.get("viewmarkauditform")
            option = request.POST.get("choices")
            if name == "Submit" and option == "1":
                success = "Audit Marked Succesfully"
                obj = fm_ptctrans.objects.filter(id=id)

                for i in obj:
                    obj = i
                    break
                obj.ptcAudited = 1
                obj.save()
                return render(request,"ViewMarkAudit.html",{'success':success})
            elif name == "Submit" and option == "2":
                success = 'Marking the Audit is cancelled'
                obj = fm_ptctrans.objects.filter(id=id)

                for i in obj:
                    obj = i
                    break
                obj.ptcAudited = 0
                obj.save()
                return render(request,"ViewMarkAudit.html",{'success':success})
            else:
                error = "there is some error while processing input given."
        else:
            error = "Invalid Input Found"
    return render(request,"ViewMarkAudit.html",{'error':error})

def ViewProject(request):
    if request.method == "GET":
        form = ptcprojectform()
        return render(request, "ViewProject.html",{'form':form})
    if request.method == "POST":
        form = ptcprojectform(request.POST)
        if form.is_valid():
            try:
                project_obj = fm_project.objects.filter(id = request.POST["prID"])
                budget_obj = fm_budgethead.objects.filter(prID = project_obj[0])
                project_status = {}
                for i in budget_obj:
                    value_sum = i.bhBalance
                    ptctrans_obj = fm_ptctrans.objects.filter(ptctransHead = i)
                    for j in ptctrans_obj:
                        value_sum = value_sum + j.ptctransValue
                    # print(i, "-", value_sum, "-", i.bhLimit)
                    project_status[i] = [i.bhLimit,value_sum]
                print(project_status)
                return render(request, "ViewProject.html",{'project_status':project_status})
            except Exception as e:
                error = e
        else:
            error = 'There is some error in input given'
        return render(request, "ViewProject.html", {'error' : error})
    return render(request, "ViewProject.html")
