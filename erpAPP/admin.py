from django.contrib import admin
from .models import fm_txn
# Register your models here.
models = [fm_txn,]
admin.site.register(models)
