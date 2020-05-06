# Generated by Django 3.0.3 on 2020-05-05 12:42

from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0003_auto_20200505_1226"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="unit_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="in $",
                max_digits=12,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0.001"))],
            ),
        ),
    ]