from django.contrib import admin
from .models import fm_txn,fm_utrans
# Register your models here.
models = [fm_txn,fm_utrans]
admin.site.register(models)
