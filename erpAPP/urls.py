from django.urls import path
from . import views
urlpatterns = [
    path("account-type/",views.AccountType.as_view(),name="account_type"),
    # path("upload-csv/",views.csv_upload,name="csv_upload"),
]
