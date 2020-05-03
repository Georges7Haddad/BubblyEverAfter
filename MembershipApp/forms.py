from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, widgets

from MembershipApp.models import Ticket, VehiclePass, Accommodation, Burn


class BubblyMemberForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "username",
            "birthday",
            "phone_number",
            "country",
            "city",
            "gender_identity",
            "ethnic_identity",
            "photo",
            "paypal_email",
            "is_virgin_burner",
            "playa_name",
            "burning_man_profile_email",
            "years_attending_burning_man",
            "referring_member",
            "facebook",
            "allergies",
            "medical_issues",
        ]


class MemberSearchForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Username"}))
    fields = [
        "username",
    ]


class YearFilterForm(forms.Form):
    year = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Year"}))
    fields = [
        year,
    ]


class YearGroupForm(forms.Form):
    GROUP_CHOICES = (
        ("Burn", "Burn"),
        ("Accommodation", "Accommodation"),
    )
    group = forms.ChoiceField(choices=GROUP_CHOICES, label="")
    year = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Year"}))
    fields = [
        year,
        group,
    ]


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "member",
            "secured",
            "status",
            "number",
            "price",
        ]


class CustomCheckboxWidget(widgets.CheckboxInput):
    template_name = "MembershipApp/checkbox.html"


class VehiclePassForm(ModelForm):
    tow_hitch = forms.BooleanField(widget=CustomCheckboxWidget)

    class Meta:
        model = VehiclePass
        fields = [
            "member",
            "secured",
            "needed",
            "ride_share",
            "number",
            "make",
            "model",
            "price",
        ]


class AccommodationForm(ModelForm):
    class Meta:
        model = Accommodation
        fields = [
            "name",
            "type",
            "is_full",
        ]


class BurnForm(ModelForm):
    class Meta:
        model = Burn
        fields = [
            "member",
            "vehicle_pass",
            "ticket",
            "year",
            "arrival_time",
            "departure_time",
            "transportation",
            "camp_dues",
            "camp_dues_paid",
            "strike_deposit",
            "strike_deposit_paid",
            "meal_plan",
            "meal_plan_paid",
            "notes",
        ]
