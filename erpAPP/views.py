from django.shortcuts import render
import csv, io
from django.contrib import messages
from .models import csv_fm_txn

# Create your views here.

def csv_upload(request):
    template = 'csv_upload.html'
    order = 'Order of the CSV should be: '
    if request.method == "GET":
        return render(request, template, {'order':order})
    csv_file = request.FILES['file']
    #Checking if file is of type CSV or not
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV file')
    jsvalue = request.POST.get('val')
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
        # obj = csv_fm_txn.objects.order_by('transc_time').reverse()
        # obj = obj[:2]



    context = {}    #'obj':obj
    return render(request, template, context)
