# Generated by Django 3.0.5 on 2020-04-18 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20200417_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]