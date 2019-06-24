from django.contrib import admin
from .models import fm_txn,fm_utrans,fm_user_extend,fm_project,fm_budgethead,fm_ptcform,fm_ptctrans
# Register your models here.
models = [fm_txn,fm_utrans,fm_user_extend,fm_project,fm_budgethead,fm_ptcform,fm_ptctrans]
admin.site.register(models)
