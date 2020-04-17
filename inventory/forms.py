from django import forms
from .models import *


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "member",
            "title",
            "description",
            "width",
            "height",
            "length",
            "quantity",
            "unit_price",
            "picture",
        ]


class AddElectricalItemForm(forms.ModelForm):
    class Meta:
        model = ElectricalItem
        fields = [
            "member",
            "title",
            "description",
            "width",
            "height",
            "length",
            "quantity",
            "unit_price",
            "picture",
            "voltage",
            "wattage",
        ]
