from django.urls import path
from . import views
urlpatterns = [
    path("account-type/",views.AccountType.as_view(),name="account_type"),
    path("complete-transaction/",views.CompleteTransaction,name="transaction_complete"),
    path("transferMoney/",views.transferMoney.as_view(), name='transferMoney'),
    # path("upload-csv/",views.csv_upload,name="csv_upload")
]
