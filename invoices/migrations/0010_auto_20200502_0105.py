# Generated by Django 3.0.3 on 2020-05-01 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0009_auto_20200502_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='receipt',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
