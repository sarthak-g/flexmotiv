from django.urls import path
from . import views
urlpatterns = [
    path("account-type/",views.AccountType.as_view(),name="account_type"),
    path("complete-transaction/",views.CompleteTransaction,name="transaction_complete"),
    path("transferMoney/",views.transferMoney.as_view(), name='transferMoney'),
    path("financialAccount/",views.financialAccount, name='financialAccount'),
    path("financialAccount/accept/<int:pk>/",views.accept, name='accept'),
    path("financialAccount/decline/<int:pk>/",views.decline, name='decline'),
    path("add-project/",views.addproject.as_view(), name='addproject'),
    path("add-project-print/",views.ProjectSuccessPDFView.as_view(), name='addprojectpdf'),

]
