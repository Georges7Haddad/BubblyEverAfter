from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.
class Invoice(models.Model):
    title = models.CharField(max_length=100)
    rate = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    receipt = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


def __str__(self):
    return {self.title}


def __repr__(self):
    return {self.title}
