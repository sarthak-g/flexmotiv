from django.contrib import admin
from .models import fm_txn,fm_utrans,fm_user_extend
# Register your models here.
models = [fm_txn,fm_utrans,fm_user_extend]
admin.site.register(models)
