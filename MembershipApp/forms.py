from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


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
