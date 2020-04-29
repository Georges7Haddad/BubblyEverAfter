from django import forms
from . import models



class CreateInvoice(forms.ModelForm):
    class Meta:
        model = models.Invoice
        fields = ['title', 'rate', 'quantity']

class UploadReceipt(forms.ModelForm):
    """Image upload form."""
    class Meta:
        model = models.Invoice
        fields = ['receipt']