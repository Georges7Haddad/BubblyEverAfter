from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Contact, BubblyEvents


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
        model = BubblyEvents
        fields = [
            "name",
            "location",
            "start_date",
            "end_date",
            "description",
            "facebook_link",
        ]
