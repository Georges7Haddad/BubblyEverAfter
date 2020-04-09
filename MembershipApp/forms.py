from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class BubblyMemberForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "birthday",
            "gender_identity",
            "ethnic_identity",
            "country",
            "city",
            "photo",
            "facebook",
            "phone_number",
            "paypal_email",
            "playa_name",
            "burning_man_profile_email",
            "is_virgin_burner",
            "years_attending_burning_man",
            "referring_member",
            "allergies",
            "medical_issues",
            "username",
        ]


class MemberSearchForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
        ]
