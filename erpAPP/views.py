from django.shortcuts import render
import csv, io
from django.contrib import messages
from .models import csv_model

# Create your views here.

def csv_upload(request):
    template = 'csv_upload.html'
    prompt = {
        'order': 'Order of the CSV should be S.no,Transaction Id,Value Date,Txn Posted Date,ChequeNo.,Description,Cr/Dr,Transaction Amount,Available Balance(INR)'
    }
    if request.method == "GET":
        return render(request, template, prompt)
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
        _, created = csv_model.objects.update_or_create(
            trans_account = column[0],
            trans_id = column[1],
            trans_date = column[2],
            trans_posted_date = column[3],
            trans_cheque = column[4],
            trans_desc = column[5],
            cr_or_dr = column[6],
            value = column[7],
            balance = column[8]
        )
    context = {}
    return render(request, template, context)
