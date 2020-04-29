from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from .models import Invoice
from . import forms


# Create your views here.
def invoices_list(request):
    invoices = Invoice.objects.all().order_by('date')
    temp = 0
    for i in Invoice.objects.all():
        temp = temp + i.rate * i.quantity
    return render(request, 'invoices/invoices_list.html', {'invoices':invoices, 'temp':temp})

def add_invoice(request):
    if request.method == 'POST':
        form = forms.CreateInvoice(request.POST)
        if form.is_valid():
            instance = form.save()
            return redirect('invoices:list')
    else:
        form = forms.CreateInvoice()
    return render(request,'invoices/invoice_add.html', {'form':form})

def view_invoice(request,int):
   invoice = Invoice.objects.get(id=int)
   return render(request, 'invoices/invoice_details.html', {'invoice':invoice})

def upload_receipt(request,int):
    if request.method == 'POST':
        form = forms.UploadReceipt(request.POST, request.FILES)
        if form.is_valid():
            m = Invoice.objects.get(id=int)
            m.receipt = form.cleaned_data['receipt']
            m.save()
            return redirect('invoices:list')