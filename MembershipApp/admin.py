from django.apps import apps
from django.contrib import admin
from inventory.models import Category,Item

app = apps.get_app_config("MembershipApp")

for model_name, model in app.models.items():
    admin.site.register(model)

admin.site.register(Category)
admin.site.register(Item)
