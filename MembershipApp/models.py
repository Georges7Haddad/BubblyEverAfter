# Create your models here.
import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ImageField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


def max_value_current_year(value):
    return MaxValueValidator(datetime.date.today().year)(value)


optional = {"null": True, "blank": True, "default": None}
required = {"null": False, "blank": False}


class BubblyMember(AbstractUser):
    # Personal info
    username = models.CharField(max_length=127, unique=True)
    is_leadership = models.BooleanField(default=False)
    birthday = models.DateField(**required)
    gender_identity = models.CharField(max_length=127, help_text="To ensure camp diversity", **optional)
    ethnic_identity = models.CharField(max_length=127, help_text="To ensure camp diversity", **optional)
    country = CountryField(**required)
    city = models.CharField(max_length=127, **required)
    photo = ImageField(**optional)

    # contact info
    facebook = models.URLField(max_length=1023, **optional)
    phone_number = PhoneNumberField(**required)
    paypal_email = models.EmailField(**required)
    verified_email = models.BooleanField(default=False)

    playa_name = models.CharField(max_length=127, **optional)
    burning_man_profile_email = models.EmailField(
        **required, help_text="Burning Man profile email address (MUST match https://profiles.burningman.org/ email)",
    )
    is_virgin_burner = models.BooleanField(default=True)
    years_attending_burning_man = models.CharField(
        max_length=127, help_text="Please separate them with commas", **optional
    )

    referring_member = models.ForeignKey("self", on_delete=models.SET_NULL, **optional)
    # health
    allergies = models.TextField(**optional)
    medical_issues = models.TextField(**optional)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["birthday", "country", "city", "phone_number", "paypal_email", "burning_man_profile_email"]

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username


class Ticket(models.Model):
    """
    This model stores the ticket information that allows you to enter to burning man
    """

    # todo implement ticket transfer
    # todo abstract ticket and vehicle pass common fields
    STATUS_CHOICES = [
        (i, i)
        for i in [
            "Pre Sale",
            "Main Sale",
            "DGS",
            "OMG Sale",
            "Low Income Approved",
            "STEP",
            "Third Party (Friend/Seller)",
        ]
    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **required,
        help_text="Name of the current vehicle pass holder",
    )
    secured = models.BooleanField(default=False, help_text="Please tick if you have a ticket ")
    status = models.CharField(max_length=127, choices=STATUS_CHOICES)
    number = models.CharField(max_length=127, **optional, help_text="ID number found on the back of your ticket", )

    price = models.PositiveIntegerField(**optional)

    def save(self, *args, **kwargs):
        if self.secured:
            if not self.number:
                raise ValidationError(f"Since you secured a ticket, please enter the ticket's number")
            if not self.price:
                raise ValidationError(f"Since you secured a ticket, please enter the ticket's price")
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.member}'s {self.number} Ticket"

    def __repr__(self):
        return f"{self.member}'s {self.number} Ticket"


class VehiclePass(models.Model):
    """
    This model stores the ticket information that allows you to bring a vehicle to burning man.
    It's separate from the ticket information
    """

    TYPE_CHOICES = [
        (i, i)
        for i in ["Small Car (hatchback)", "Mid Sized Car", "Van", "SUV", "PickUp Truck", "Small RV", "Large RV", ]
    ]
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **required,
        help_text="Name of the current vehicle pass holder",
    )
    secured = models.BooleanField(help_text="Please tick if you have a vehicle pass", default=False)
    needed = models.BooleanField(help_text="Please tick if you need a vehicle pass", default=False)
    ride_share = models.PositiveIntegerField(help_text="Number of extra room with you", **required)
    number = models.CharField(max_length=127, **optional, help_text="ID number found on the back of your ticket",)
    make = models.CharField(max_length=127, **optional)
    model = models.CharField(max_length=127, **optional)
    tow_hitch = models.BooleanField(default=False, help_text="Please tick if you have a tow hitch")

    price = models.PositiveIntegerField(**optional)

    def save(self, *args, **kwargs):
        if self.secured:
            if not self.number:
                raise ValidationError(f"Since you secured a Vehicle Pass, please enter the vehicle pass' number")
            if not self.price:
                raise ValidationError(f"Since you secured a Vehicle Pass, please enter the vehicle pass' number")
        super(VehiclePass, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.member}'s {self.number} VehiclePass"

    def __repr__(self):
        return f"{self.member}'s {self.number} VehiclePass"


class Accommodation(models.Model):
    """
    This models stores information about a camping member's accommodation during this year's burn(camp)
    """

    ACCOMMODATION_CHOICES = [
        (i, i)
        for i in [
            "RV",
            "Travel Trailer",
            "Shiftpod",
            "Kodiak Tent",
            "No Bake Tent",
            "Siesta2 Tent",
            "Siesta4 Tent",
            "Small Tent (Under 10'x10')",
            "Medium Tent (Fits in 10'x10')",
            "Large Tent (Larger than 10'x10')",
            "Other",
        ]
    ]
    name = models.CharField(max_length=127, **required)
    type = models.CharField(max_length=127, choices=ACCOMMODATION_CHOICES)
    is_full = models.BooleanField(default=False)

    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserAccommodationRelation")

    def __str__(self):
        return f"{self.name}'s Accommodation"

    def __repr__(self):
        return f"{self.name}'s Accommodation"


class UserAccommodationRelation(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **required)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, **required)

    def __str__(self):
        return f"{self.member} is staying in {self.accommodation}"

    def __repr__(self):
        return f"{self.member} is staying in {self.accommodation}"


class Burn(models.Model):
    """
    Model containing information for each member's burn(burning man event)
    """

    accommodations = models.ManyToManyField(Accommodation, through="BurnAccommodationRelation")
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **required)

    # In case someone has many vehicle pass he chooses the one he's going with
    vehicle_pass = models.OneToOneField(VehiclePass, on_delete=models.CASCADE, **optional)

    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, **required)

    year = models.PositiveIntegerField(validators=[MinValueValidator(1984), max_value_current_year], **required)

    arrival_time = models.DateTimeField(**optional)
    departure_time = models.DateTimeField(**optional)

    TRANSPORTATION_CHOICES = [
        (i, i) for i in
        ["Burner Air", "Burner Bus", "Carpool", "Own Transportation (will need vehicle pass)", "Other", ]
    ]
    transportation = models.CharField(max_length=127, choices=TRANSPORTATION_CHOICES, **required)

    camp_dues = models.PositiveIntegerField(
        default=0, **required, help_text="Payment that each camping member should pay to join bubbly camp",
    )

    camp_dues_paid = models.PositiveIntegerField(default=0, **required)

    strike_deposit = models.PositiveIntegerField(
        default=0,
        **required,
        help_text="Payment that each camping member should pay to make sure they help cleaning before leaving",
    )
    strike_deposit_paid = models.PositiveIntegerField(default=0, **required)

    meal_plan = models.BooleanField(
        default=False, help_text="Payment that each camping member should pay to join the meal plan",
    )
    meal_plan_paid = models.PositiveIntegerField(default=0, **required)

    notes = models.TextField(**optional)

    def save(self, *args, **kwargs):
        if self.transportation == "Own Transportation (will need vehicle pass)" and not self.vehicle_pass:
            raise ValidationError(f"Please fill in the details of your vehicle pass")
        super(Burn, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.member}'s {self.year} Burn"

    def __repr__(self):
        return f"{self.member}'s {self.year} Burn"


class BurnAccommodationRelation(models.Model):
    burn = models.ForeignKey(Burn, on_delete=models.CASCADE, **required)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, **required)

    def __str__(self):
        return f"{self.burn.member} is staying in {self.accommodation} in {self.burn.year}"

    def __repr__(self):
        return f"{self.burn.member} is staying in {self.accommodation} in {self.burn.year}"
