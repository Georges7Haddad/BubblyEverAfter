# Generated by Django 3.0.3 on 2020-04-16 00:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("MembershipApp", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(model_name="ticket", old_name="holder", new_name="member", ),
        migrations.RenameField(model_name="vehiclepass", old_name="holder", new_name="member", ),
    ]
