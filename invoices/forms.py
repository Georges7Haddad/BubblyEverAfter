from django import forms
from . import models



class CreateInvoice(forms.ModelForm):
    class Meta:
        model = models.Invoice
        fields = ['title', 'price', 'quantity']

class UploadReceipt(forms.ModelForm):
    class Meta:
        model = models.Invoice
        fields = ['receipt']

class SendInvoice(forms.ModelForm):
    class Meta:
        model = models.Invoice
        fields = ['title', 'price', 'quantity','user']