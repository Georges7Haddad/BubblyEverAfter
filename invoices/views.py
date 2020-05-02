from msilib.schema import ListView

from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from .models import Invoice
from . import forms
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/member/login")
def invoices_list(request):
    invoices = Invoice.objects.filter(user=request.user).filter(Q(receipt='')|Q(receipt=None)).order_by('date')
    temp = 0
    for i in invoices:
        temp = temp + i.rate * i.quantity
    return render(request, 'invoices/invoices_list.html', {'invoices':invoices, 'temp':temp})

@login_required(login_url="/member/login")
def add_invoice(request):
    if request.method == 'POST':
        form = forms.CreateInvoice(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('invoices:list')
    else:
        form = forms.CreateInvoice()
    return render(request,'invoices/invoice_add.html', {'form':form})

def view_invoice(request,int):
   invoice = Invoice.objects.get(id=int)
   name = request.user.get_full_name()
   return render(request, 'invoices/invoice_details.html', {'invoice':invoice, 'name':name})

@login_required(login_url="/member/login")
def upload_receipt(request,int):
    if request.method == 'POST':
        form = forms.UploadReceipt(request.POST, request.FILES)
        if form.is_valid():
            m = Invoice.objects.get(id=int)
            m.receipt = form.cleaned_data['receipt']
            m.save()
            return redirect('invoices:list')