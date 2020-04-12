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
    voltage = models.PositiveIntegerField(null=True, blank=True, help_text="If it is an electrical item")
    wattage = models.PositiveIntegerField(null=True, blank=True, help_text="If it is an electrical item")
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    picture = models.FileField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return "Item: {0}".format(self.title)


class Category(models.Model):
    name = models.CharField(max_length=127)
    items = models.ManyToManyField(Item,blank=True)

    def __str__(self):
        return "Category: {0}".format(self.name)