from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, widgets

from MembershipApp.models import Ticket, VehiclePass, Accommodation, Burn, Contact, BubblyEvent


class DateInput(forms.DateInput):
    input_type = "date"


class CustomCheckboxWidget(widgets.CheckboxInput):
    template_name = "MembershipApp/checkbox.html"

    def __init__(self, *args, **kwargs):
        super(CustomCheckboxWidget, self).__init__(*args, **kwargs)
        self.help_text = kwargs.get("help_text")

    def _render(self, template_name, context, renderer=None):
        context["help_text"] = self.help_text
        return super(CustomCheckboxWidget, self)._render(template_name, context, renderer)


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
        widgets = {"birthday": DateInput(), "is_virgin_burner": CustomCheckboxWidget()}


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
        widgets = {"secured": CustomCheckboxWidget()}


class VehiclePassForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehiclePassForm, self).__init__(*args, **kwargs)
        for fieldname in ["secured", "needed", "tow_hitch"]:
            self.fields[fieldname].widget = CustomCheckboxWidget(help_text=self.fields[fieldname].help_text)
            self.fields[fieldname].help_text = None

    class Meta:
        model = VehiclePass
        fields = ["member", "secured", "needed", "ride_share", "number", "make", "model", "price", "tow_hitch"]


class AccommodationForm(ModelForm):
    class Meta:
        model = Accommodation
        fields = [
            "name",
            "type",
            "is_full",
        ]
        widgets = {
            "is_full": CustomCheckboxWidget(),
        }


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
        widgets = {"arrival_time": DateInput(), "departure_time": DateInput()}


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = [
            "name",
            "playa_name",
            "email",
            "social_media",
            "Please_tell_us_3_adjectives_that_describe_you_most",
            "how_can_we_collaborate_and_get_to_know_you_better",
        ]


class CreateEvent(ModelForm):
    class Meta:
        model = BubblyEvent
        fields = [
            "name",
            "location",
            "start_date",
            "end_date",
            "description",
            "facebook_link",
        ]
