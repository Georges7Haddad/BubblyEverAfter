from django.db import models

# Create your models here.
from MembershipApp.models import BubblyMember


class Item(models.Model):
    member = models.ForeignKey(BubblyMember, on_delete=models.CASCADE)
    title = models.CharField(max_length=127, blank=False)
    description = models.TextField()
    width = models.PositiveIntegerField(null=True, blank=True, help_text="in meters")
    height = models.PositiveIntegerField(null=True, blank=True, help_text="in meters")
    length = models.PositiveIntegerField(null=True, blank=True, help_text="in meters")
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField(help_text="in $")
    picture = models.FileField(null=True, blank=True)

    def __str__(self):
        return "Item: {0}".format(self.title)


class ElectricalItem(Item):
    voltage = models.PositiveIntegerField(null=False, blank=False, help_text="in Volts")
    wattage = models.PositiveIntegerField(null=False, blank=False, help_text="in Watts")


class Category(models.Model):
    name = models.CharField(max_length=127)
    items_type = models.CharField(
        max_length=50,
        choices=[("non_electrical_items", "Non Electrical Items"), ("electrical_items", "Electrical Items")],
        default="non_electrical_items",
    )
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return "Category: {0}".format(self.name)
