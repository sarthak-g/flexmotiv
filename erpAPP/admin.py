from django.contrib import admin
from .models import csv_fm_txn
# Register your models here.
models = [csv_fm_txn,]
admin.site.register(models)
