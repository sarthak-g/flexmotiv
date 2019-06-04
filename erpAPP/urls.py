from django.urls import path
from . import views
urlpatterns = [
    path("upload-csv/",views.csv_upload,name="csv_upload")
]
