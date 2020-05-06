from django.urls import path

from . import views

app_name = "invoices"

urlpatterns = [
    path("", views.invoices_list, name="list"),
    path("add/", views.add_invoice, name="add"),
    path("<int:int>/", views.view_invoice, name="detail"),
    path("<int:int>/receipt/", views.upload_receipt, name="receipt"),
    path("export/", views.export_balance_sheet, name="export_sheet"),
]
