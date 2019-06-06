from django.shortcuts import render
import csv, io
from django.contrib import messages
from .models import csv_fm_txn
from django.views.generic import TemplateView
from .forms import AccountTypeForm
# Create your views here.
def account_type(request):
    return render(request,"account_type.html")

def csv_upload(request):
    template = 'csv_upload.html'
    order = 'Order of the CSV should be: '
    if request.method == "GET":
        return render(request, template, {'order':order})
    csv_file = request.FILES['file']
    #Checking if file is of type CSV or not
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV file')

    #Taking the dataset
    data_set = csv_file.read().decode('UTF-8')
    #loop through all data using streams
    io_string = io.StringIO(data_set)
    #Skipping first line of csv  as it contain headers
    next(io_string)
    for column in csv.reader(io_string, delimiter=',',quotechar="|"):
        _, created = csv_fm_txn.objects.update_or_create(
            txnID = column[0],
            accID = 0,
            txnDate = column[2],
            txnPostedDate = column[3],
            txnCheque = column[4],
            txnDir = column[5],
            txnDesc = column[6],
            txnValue = column[7],
            txnBalance = column[8],
        )



    context = {}
    return render(request, template, context)
class AccountType(TemplateView):
    template_name = "account_type.html"
    option_selected = ''
    def get(self,request):
        form = AccountTypeForm()
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = AccountTypeForm(request.POST)
        accountID = 1
        if form.is_valid():
            option_selected = form.cleaned_data['choices']
            option_selected = int(option_selected)
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
                print(obj)
            args = {'form':form,"record":record,'message':message,'obj':obj}
            return render(request, self.template_name,args)
        # if not AccountTypeForm.is_valid():
        else:
            csv_file = request.FILES['file']
            #Checking if file is of type CSV or not
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is not a CSV file')

            #Taking the dataset
            data_set = csv_file.read().decode('UTF-8')
            #loop through all data using streams
            io_string = io.StringIO(data_set)
            #Skipping first line of csv  as it contain headers
            next(io_string)
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
                )



            context = {}

            return render(request, "try.html",context)
