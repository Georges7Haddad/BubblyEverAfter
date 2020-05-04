# Generated by Django 3.0.3 on 2020-04-23 15:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=127)),
                ("description", models.TextField()),
                ("width", models.PositiveIntegerField(blank=True, help_text="in meters", null=True)),
                ("height", models.PositiveIntegerField(blank=True, help_text="in meters", null=True)),
                ("length", models.PositiveIntegerField(blank=True, help_text="in meters", null=True)),
                ("quantity", models.PositiveIntegerField()),
                ("unit_price", models.PositiveIntegerField(help_text="in $")),
                ("picture", models.FileField(blank=True, null=True, upload_to="")),
                ("member", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ElectricalItem",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="inventory.Item",
                    ),
                ),
                ("voltage", models.PositiveIntegerField(help_text="in Volts")),
                ("wattage", models.PositiveIntegerField(help_text="in Watts")),
            ],
            bases=("inventory.item",),
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=127)),
                (
                    "items_type",
                    models.CharField(
                        choices=[
                            ("non_electrical_items", "Non Electrical Items"),
                            ("electrical_items", "Electrical Items"),
                        ],
                        default="non_electrical_items",
                        max_length=50,
                    ),
                ),
                ("items", models.ManyToManyField(blank=True, to="inventory.Item")),
            ],
        ),
    ]
