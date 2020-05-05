from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from MembershipApp.models import BubblyMember


class Item(models.Model):
    member = models.ForeignKey(BubblyMember, on_delete=models.CASCADE)
    title = models.CharField(max_length=127, blank=False)
    description = models.TextField()
    width = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=3,
        max_digits=12,
        help_text="in meters",
        validators=[MinValueValidator(Decimal("0.001"))],
    )
    height = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=3,
        max_digits=12,
        help_text="in meters",
        validators=[MinValueValidator(Decimal("0.001"))],
    )
    length = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=3,
        max_digits=12,
        help_text="in meters",
        validators=[MinValueValidator(Decimal("0.001"))],
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        help_text="in $",
        validators=[MinValueValidator(Decimal("0.001"))],
    )
    picture = models.FileField(null=True, blank=True)

    def __str__(self):
        return "Item: {0}".format(self.title)


class ElectricalItem(Item):
    voltage = models.DecimalField(
        null=False,
        blank=False,
        help_text="in Volts",
        decimal_places=3,
        max_digits=12,
        validators=[MinValueValidator(Decimal("0.001"))],
    )
    wattage = models.DecimalField(
        null=False,
        blank=False,
        help_text="in Watts",
        decimal_places=3,
        max_digits=12,
        validators=[MinValueValidator(Decimal("0.001"))],
    )


class Category(models.Model):
    name = models.CharField(max_length=127)
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return "Category: {0}".format(self.name)
