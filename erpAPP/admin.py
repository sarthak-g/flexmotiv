from django.contrib import admin
from .models import csv_fm_txn,CSVfileStorage
# Register your models here.
models = [csv_fm_txn,CSVfileStorage]
admin.site.register(models)
