from django.forms import ModelForm

from .models import BubblyMember


class BubblyMemberForm(ModelForm):
    class Meta:
        model = BubblyMember
        fields = [
            'birthday',
            'gender_identity',
            'ethnic_identity',
            'country',
            'city',
            'photo',
            'facebook',
            'phone_number',
            'paypal_email',
            'playa_name',
            'burning_man_profile_email',
            'is_virgin_burner',
            'years_attending_burning_man',
            'referring_member',
            'allergies',
            'medical_issues',
        ]
