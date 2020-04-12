from django import forms
from .models import Item,Category

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['member', 'title', 'description', 'width','height','length','voltage','wattage','quantity','unit_price','picture']

