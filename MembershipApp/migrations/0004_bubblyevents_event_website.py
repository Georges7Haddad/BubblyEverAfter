# Generated by Django 3.0.3 on 2020-04-19 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("MembershipApp", "0003_auto_20200419_1549"),
    ]

    operations = [
        migrations.AddField(
            model_name="bubblyevents",
            name="event_website",
            field=models.CharField(blank=True, default=None, max_length=1023, null=True),
        ),
    ]
