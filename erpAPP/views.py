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
        jsvalue = request.GET.get["val"]
        return render(request, template, {'order':order,'jsvalue':jsvalue})
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
            accID = 1,
            txnDate = column[2],
            txnPostedDate = column[3],
            txnCheque = column[4],
            txnDir = column[5],
            txnDesc = column[6],
            txnValue = column[7],
            txnBalance = column[8],
        )
        obj = csv_fm_txn.objects.order_by('transc_time').reverse()
        obj = obj[:2]


    context = {'obj':obj,'jsvalue':jsvalue}
    return render(request, template, context)
class AccountType(TemplateView):
    template_name = "account_type.html"
    def get(self,request):
        form = AccountTypeForm()
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = AccountTypeForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['choices']
        args = {'form':form, 'text':text}
        return render(request, self.template_name,args)
