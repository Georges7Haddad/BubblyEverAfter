import csv

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import forms
from .models import Invoice


# Create your views here.
@login_required(login_url="/member/login")
def invoices_list(request):
    if request.user.is_superuser:
        invoices = Invoice.objects.order_by("date")
        temp = 0
        for i in invoices:
            temp = temp + i.price * i.quantity
            if i.receipt == "":
                i.status = "Pending Receipt"
                i.save()
            else:
                i.status = "Completed"
                i.save()

        return render(request, "invoices/lead_invoices_list.html", {"invoices": invoices, "temp": temp})
    else:
        # invoices = Invoice.objects.filter(user=request.user).filter(Q(receipt='')|Q(receipt=None)).order_by('date')
        invoices = Invoice.objects.filter(user=request.user).order_by("date")
        temp = 0
        for i in invoices:
            temp = temp + i.price * i.quantity
            if i.receipt == "":
                i.status = "Pending Receipt"
                i.save()
            else:
                i.status = "Completed"
                i.save()

        return render(request, "invoices/invoices_list.html", {"invoices": invoices, "temp": temp})


@login_required(login_url="/member/login")
def add_invoice(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = forms.SendInvoice(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect("invoices:list")
        else:
            form = forms.SendInvoice()
        return render(request, "invoices/lead_invoice_add.html", {"form": form})
    else:
        if request.method == "POST":
            form = forms.CreateInvoice(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return redirect("invoices:list")
        else:
            form = forms.CreateInvoice()
        return render(request, "invoices/invoice_add.html", {"form": form})


def view_invoice(request, int):
    if request.user.is_superuser:
        invoice = Invoice.objects.get(id=int)
        if invoice.receipt == "":
            name = request.user.get_full_name()
            return render(request, "invoices/lead_pending_invoice_details.html", {"invoice": invoice, "name": name})
        else:
            invoice = Invoice.objects.get(id=int)
            name = request.user.get_full_name()
            return render(request, "invoices/lead_invoice_details.html", {"invoice": invoice, "name": name})
    else:
        invoice = Invoice.objects.get(id=int)
        if invoice.receipt == "":
            invoice = Invoice.objects.get(id=int)
            name = request.user.get_full_name()
            return render(request, "invoices/invoice_details.html", {"invoice": invoice, "name": name})
        else:
            invoice = Invoice.objects.get(id=int)
            name = request.user.get_full_name()
            return render(request, "invoices/invoice_completed_details.html", {"invoice": invoice, "name": name})


@login_required(login_url="/member/login")
def upload_receipt(request, int):
    if request.method == "POST":
        form = forms.UploadReceipt(request.POST, request.FILES)
        if form.is_valid():
            m = Invoice.objects.get(id=int)
            m.receipt = form.cleaned_data["receipt"]
            m.save()
            return redirect("invoices:list")


@login_required(login_url="/member/login")
def export_balance_sheet(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachement; filename="balance_sheet.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Quantity", "Price", "Total"])

    invoices = Invoice.objects.filter(user=request.user).filter(Q(receipt="") | Q(receipt=None)).order_by("date")

    sum = 0

    for i in invoices:
        sum = sum + i.price * i.quantity

    for invoice in invoices:
        writer.writerow(
            [invoice.title, invoice.quantity, "$" + str(invoice.price), "$" + str(invoice.price * invoice.quantity)]
        )

    writer.writerow(["Total Cost", "", "", "$" + str(sum)])

    return response
