import django.contrib.auth.models
import django.core.validators
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models

import MembershipApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
    ]

    operations = [
        migrations.CreateModel(
            name="Accommodation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=127)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("RV", "RV"),
                            ("Travel Trailer", "Travel Trailer"),
                            ("Shiftpod", "Shiftpod"),
                            ("Kodiak Tent", "Kodiak Tent"),
                            ("No Bake Tent", "No Bake Tent"),
                            ("Siesta2 Tent", "Siesta2 Tent"),
                            ("Siesta4 Tent", "Siesta4 Tent"),
                            ("Small Tent (Under 10'x10')", "Small Tent (Under 10'x10')"),
                            ("Medium Tent (Fits in 10'x10')", "Medium Tent (Fits in 10'x10')"),
                            ("Large Tent (Larger than 10'x10')", "Large Tent (Larger than 10'x10')"),
                            ("Other", "Other"),
                        ],
                        max_length=127,
                    ),
                ),
                ("is_full", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Burn",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "year",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1984),
                            MembershipApp.models.max_value_current_year,
                        ]
                    ),
                ),
                ("arrival_time", models.DateTimeField(blank=True, default=None, null=True)),
                ("departure_time", models.DateTimeField(blank=True, default=None, null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Burner Air", "Burner Air"),
                            ("Burner Bus", "Burner Bus"),
                            ("Carpool", "Carpool"),
                            (
                                "Own Transportation (will need vehicle pass)",
                                "Own Transportation (will need vehicle pass)",
                            ),
                            ("Other", "Other"),
                        ],
                        max_length=127,
                    ),
                ),
                (
                    "camp_dues",
                    models.PositiveIntegerField(
                        default=0, help_text="Payment that each camping member should pay to join bubbly camp"
                    ),
                ),
                ("camp_dues_paid", models.PositiveIntegerField(default=0)),
                (
                    "strike_deposit",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Payment that each camping member should pay to make sure they help cleaning before leaving",
                    ),
                ),
                ("strike_deposit_paid", models.PositiveIntegerField(default=0)),
                (
                    "meal_plan",
                    models.BooleanField(
                        default=False, help_text="Payment that each camping member should pay to join the meal plan"
                    ),
                ),
                ("meal_plan_paid", models.PositiveIntegerField(default=0)),
                ("notes", models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="BubblyMember",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=30, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="email address")),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("username", models.CharField(max_length=127, unique=True)),
                ("is_leadership", models.BooleanField(default=False)),
                ("birthday", models.DateField()),
                (
                    "gender_identity",
                    models.CharField(
                        blank=True, default=None, help_text="To ensure camp diversity", max_length=127, null=True
                    ),
                ),
                (
                    "ethnic_identity",
                    models.CharField(
                        blank=True, default=None, help_text="To ensure camp diversity", max_length=127, null=True
                    ),
                ),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("city", models.CharField(max_length=127)),
                ("photo", models.ImageField(blank=True, default=None, null=True, upload_to="")),
                ("facebook", models.URLField(blank=True, default=None, max_length=1023, null=True)),
                ("phone_number", phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ("paypal_email", models.EmailField(max_length=254)),
                ("verified_email", models.BooleanField(default=False)),
                ("playa_name", models.CharField(blank=True, default=None, max_length=127, null=True)),
                (
                    "burning_man_profile_email",
                    models.EmailField(
                        help_text="Burning Man profile email address (MUST match https://profiles.burningman.org/ email)",
                        max_length=254,
                    ),
                ),
                ("is_virgin_burner", models.BooleanField(default=True)),
                (
                    "years_attending_burning_man",
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text="Please separate them with commas",
                        max_length=127,
                        null=True,
                    ),
                ),
                ("allergies", models.TextField(blank=True, default=None, null=True)),
                ("medical_issues", models.TextField(blank=True, default=None, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "referring_member",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"verbose_name": "user", "verbose_name_plural": "users", "abstract": False,},
            managers=[("objects", django.contrib.auth.models.UserManager()),],
        ),
        migrations.CreateModel(
            name="VehiclePass",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("secured", models.BooleanField(default=False, help_text="Please tick if you have a vehicle pass")),
                ("needed", models.BooleanField(default=False, help_text="Please tick if you need a vehicle pass")),
                ("ride_share", models.PositiveIntegerField(help_text="Number of extra room with you")),
                (
                    "number",
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text="ID number found on the back of your ticket",
                        max_length=127,
                        null=True,
                    ),
                ),
                ("make", models.CharField(blank=True, default=None, max_length=127, null=True)),
                ("model", models.CharField(blank=True, default=None, max_length=127, null=True)),
                ("tow_hitch", models.BooleanField(default=False, help_text="Please tick if you have a tow hitch")),
                ("price", models.PositiveIntegerField(blank=True, default=None, null=True)),
                (
                    "holder",
                    models.ForeignKey(
                        help_text="Name of the current vehicle pass holder",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserAccommodationRelation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "accommodation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="MembershipApp.Accommodation"),
                ),
                ("member", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("secured", models.BooleanField(default=False, help_text="Please tick if you have a ticket ")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pre Sale", "Pre Sale"),
                            ("Main Sale", "Main Sale"),
                            ("DGS", "DGS"),
                            ("OMG Sale", "OMG Sale"),
                            ("Low Income Approved", "Low Income Approved"),
                            ("STEP", "STEP"),
                            ("Third Party (Friend/Seller)", "Third Party (Friend/Seller)"),
                        ],
                        max_length=127,
                    ),
                ),
                (
                    "number",
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text="ID number found on the back of your ticket",
                        max_length=127,
                        null=True,
                    ),
                ),
                ("price", models.PositiveIntegerField(blank=True, default=None, null=True)),
                (
                    "holder",
                    models.ForeignKey(
                        help_text="Name of the current vehicle pass holder",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BurnAccommodationRelation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "accommodation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="MembershipApp.Accommodation"),
                ),
                ("burn", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="MembershipApp.Burn")),
            ],
        ),
        migrations.AddField(
            model_name="burn",
            name="accommodations",
            field=models.ManyToManyField(
                through="MembershipApp.BurnAccommodationRelation", to="MembershipApp.Accommodation"
            ),
        ),
        migrations.AddField(
            model_name="burn",
            name="member",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="burn",
            name="ticket",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="MembershipApp.Ticket"),
        ),
        migrations.AddField(
            model_name="burn",
            name="vehicle_pass",
            field=models.OneToOneField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="MembershipApp.VehiclePass",
            ),
        ),
        migrations.AddField(
            model_name="accommodation",
            name="members",
            field=models.ManyToManyField(
                through="MembershipApp.UserAccommodationRelation", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
