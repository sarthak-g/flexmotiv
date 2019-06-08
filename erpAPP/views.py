from django.shortcuts import render
import csv, io
from django.contrib import messages
from .models import csv_fm_txn,CSVfileStorage
from django.views.generic import TemplateView
from .forms import AccountTypeForm, CSVFileForm
import os.path
from django.conf import settings
from django.db import IntegrityError
# Create your views here.
def account_type(request):
    return render(request,"account_type.html")

def csv_upload(request):
    template = 'csv_upload.html'
    order = 'Order of the CSV should be: '
    if request.method == "GET":
        return render(request, template, {'order':order})
    context = {}
    return render(request, template, context)


class AccountType(TemplateView):
    template_name = "account_type.html"
    option_selected = ''
    accountID = 0
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
            record  = csv_fm_txn.objects.filter(accID=option_selected)
            message = ''
            obj = None
            if record.count()==0:   #  count=0 i.e. no record present for particular account type
                message = 'No record corresponding to this account type is present.'
            else:
                obj = record
                obj = obj.order_by('transc_time').reverse()
                obj = obj[:2]
            args = {'form':form,"record":record,'message':message,'obj':obj,'show_csv':show_csv}
            return render(request, self.template_name,args)
        # if not AccountTypeForm.is_valid():
        else:

            csv_file = request.FILES['file']
            #Checking if file is of type CSV or not
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is not a CSV file')


            destination = settings.MEDIA_ROOT + '/file_link/'
            if os.path.isfile(destination + str(csv_file)):
                print("file with same name already exists")
            else:
                result = ''
                duplicate = 0
                imported = 0
                # print("file not exists")


                #Taking the dataset
                data_set = csv_file.read().decode('UTF-8')
                #loop through all data using streams
                io_string = io.StringIO(data_set)
                #Skipping first line of csv  as it contain headers
                next(io_string)
                #generate any 4-5 digit no here and store that in place of file link
                try:
                    for column in csv.reader(io_string, delimiter=',',quotechar="|"):
                        _, created = csv_fm_txn.objects.update_or_create(
                            txnID = column[0],
                            accID = accountID,
                            txnDate = column[2],
                            txnPostedDate = column[3],
                            txnCheque = column[4],
                            txnDir = column[5],
                            txnDesc = column[6],
                            txnValue = column[7],
                            txnBalance = column[8],
                            txnAuditFile = csv_file,

                        )
                        if created == True:
                            imported = imported + 1
                        else:
                            duplicate = duplicate + 1
                        # total transaction = imported + duplicate

                    CSVfileStorage.objects.create(txnAuditFileStorage=csv_file)
                    result = 'success,file is imported'
                except IntegrityError as e:      #IntegrityError - Error for primary key
                    print(e)
                    print("same Transaction ID exists in database")
                    result = 'unsuccess,file is not imported'
                # if created:
                #     result = 'transaction is successful'
                # else:
                #     result = 'transaction is unsuccessful'
                context = {'show_csv':show_csv,'result':result,'imported':imported,'duplicate':duplicate}
                print(context)


            return render(request, "try.html")
def CompleteTransaction(request):
    untagged_objects = csv_fm_txn.objects.filter(txnType='U')
    return render(request,'CompleteTransaction.html',{'untagged_objects':untagged_objects})
