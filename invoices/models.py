from django.db import models


# Create your models here.
class Invoice(models.Model):
    title = models.CharField(max_length=100)
    rate = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    receipt = models.ImageField(blank=True)


def __str__(self):
    return {self.title}


def __repr__(self):
    return {self.title}
