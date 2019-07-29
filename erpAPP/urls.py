from django.urls import path
from . import views
urlpatterns = [
    path("account-type/",views.AccountType.as_view(),name="account_type"),
    # path("complete-transaction/",views.CompleteTransaction,name="transaction_complete"),
    path("transferMoney/",views.transferMoney.as_view(), name='transferMoney'),
    path("transferMoney/success/",views.transferMoneysuccess, name='transferMoneysuccess'),
    path("financialAccount/",views.financialAccount, name='financialAccount'),
    path("financialAccount/accept/<int:pk>/",views.accept, name='accept'),
    path("financialAccount/decline/<int:pk>/",views.decline, name='decline'),
    path("add-project/",views.addproject.as_view(), name='addproject'),
    path("add-project-print/",views.ProjectSuccessPDFView.as_view(), name='addprojectpdf'),
    path("ptc-project/",views.ptcproject, name='ptc_project'),
    path("check-statement/",views.CheckStatement, name='check-statement'),
    path("check-statement/categorize/<str:txnID>/",views.Categorize, name='categorize'),
    path("check-statement/categorize/<str:txnID>/<int:pk>/",views.CategorizeExpense, name='categorize'),
    path("view-statement/",views.ViewStatement, name='view-statement'),
    path("view-statement/<int:id>/mark-audit/",views.ViewMarkAudit, name='mark-audit-statement'),
    path("view-statement/<int:id>/mark-account/",views.ViewMarkAccount, name='view-mark-statement'),
    path("view-statement/<int:ptcID>/expense-list/",views.ExpenseList, name='expense-list'),
    path("view-statement/mark-account/<str:txnID>/",views.MarkAccount, name='mark-account'),
    path("view-project/",views.ViewProject, name='view-project'),
]
