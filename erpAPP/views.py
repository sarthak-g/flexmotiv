from django.shortcuts import render
import csv, io
from django.contrib import messages
from .models import fm_txn,fm_utrans,fm_user_extend,fm_project,fm_budgethead
from django.views.generic import TemplateView
from .forms import AccountTypeForm,TransferMoneyForm,AddProjectForm,ProjectBudgetForm,ProjectBudgetForm2,ProjectBudgetForm3,ProjectBudgetForm4,ProjectBudgetForm5,ProjectBudgetForm6,ProjectBudgetForm7,ProjectBudgetForm8,ProjectBudgetForm9,ProjectBudgetForm10,ptcprojectform
import os.path
from django.conf import settings
from django.db import IntegrityError
import uuid
import os.path
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from easy_pdf.views import PDFTemplateView



# Create your views here.
def account_type(request):
    return render(request,"account_type.html")


class AccountType(TemplateView):
    template_name = "account_type.html"
    option_selected = ''
    accountID = 0
    # accountID = 0
    show_csv = 'No'
    def get(self,request):
        form = AccountTypeForm()
        return render(request, self.template_name, {'form':form})
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

            return render(request, "pmTransactionResult.html",{'error':error})
        return render(request,self.template_name)
def CompleteTransaction(request):
    untagged_objects = fm_txn.objects.filter(txnType='U')
    return render(request,'CompleteTransaction.html',{'untagged_objects':untagged_objects})


class transferMoney(CreateView):
    model = fm_utrans
    template_name = 'transferMoney.html'
    fields = ['utranValue','utranDesc','utranReceiver']

    def form_valid(self, form):
        form.instance.utranSender = self.request.user.id
        return super(transferMoney, self).form_valid(form)
def financialAccount(request):
    record = fm_utrans.objects.filter(utranReceiver=request.user.id)
    record = record.filter(utranConfirmed='N')
    record_message = record.exists()
    overview = fm_user_extend.objects.filter(user=request.user.id)
    print(overview)
    record_confirmed = fm_utrans.objects.filter(utranConfirmed='Y')
    record_confirmed_Cr = record_confirmed.filter(utranReceiver=request.user.id)
    record_confirmed_Dr = record_confirmed.filter(utranSender=request.user.id)
    if record_confirmed_Cr.exists()==False and record_confirmed_Dr.exists()==False:
        record_confirmed_message = False
    else:
        record_confirmed_message = True
    return render(request,"financialAccount.html",{'record':record,'record_confirmed_Cr':record_confirmed_Cr,'record_confirmed_Dr':record_confirmed_Dr,'record_message':record_message,'record_confirmed_message':record_confirmed_message,'overview':overview})
def accept(request,pk):
    record = fm_utrans.objects.get(id=pk)
    record.utranConfirmed = 'Y'
    record.save()
    return render(request,"accept.html")
def decline(request,pk):
    record = fm_utrans.objects.get(id=pk)
    record.utranConfirmed = 'D'
    record.save()
    return render(request,"decline.html")

class addproject(TemplateView):
    template_name = "add_project.html"

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
    form = ptcprojectform()
    if request.method == "POST":
        print(request)
    return render(request,"ptcproject.html",{'form':form})
