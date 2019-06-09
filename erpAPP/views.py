from django.shortcuts import render
import csv, io
from django.contrib import messages
from .models import csv_fm_txn
from django.views.generic import TemplateView
from .forms import AccountTypeForm, CSVFileForm
import os.path
from django.conf import settings
from django.db import IntegrityError
import uuid
import os.path
# Create your views here.
def account_type(request):
    return render(request,"account_type.html")

# def csv_upload(request):
#     template = 'csv_upload.html'
#     order = 'Order of the CSV should be: '
#     if request.method == "GET":
#         return render(request, template, {'order':order})
#     context = {}
#     return render(request, template, context)


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
            record  = csv_fm_txn.objects.filter(accID=option_selected)
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
                last = csv_fm_txn.objects.all()
                last = last.order_by('transc_time').reverse()
                balance_temp = 1
                balance_check = 'unsuccess,file is not imported'
                if last.exists():
                    last = last.first()
                    field_object = csv_fm_txn.objects.filter(txnID=last).values('txnBalance').get()
                    field_object = field_object['txnBalance']


                for column in csv.reader(io_string, delimiter=',',quotechar="|"):
                    if balance_temp == 1:
                        print(column[8])
                        print(field_object)
                        if column[8] == str(field_object) or field_object == 0.0:
                            # checking integrity check of balance
                            balance_check = True
                            balance_temp = 0
                        else:
                            balance_check = False
                            balance_temp = 0



                    if balance_check == True:
                        try:
                            dash, created = csv_fm_txn.objects.update_or_create(
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
                print(balance_check)
                return render(request, "try.html",{'balance_check':balance_check,'result':result,'imported':imported,'duplicate':duplicate,'total_trnsactions':total_trnsactions})

            return render(request, "try.html",{'error':error})
        return render(request,self.template_name)
def CompleteTransaction(request):
    untagged_objects = csv_fm_txn.objects.filter(txnType='U')
    return render(request,'CompleteTransaction.html',{'untagged_objects':untagged_objects})
