# Generated by Django 3.0.3 on 2020-04-28 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0006_auto_20200420_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='receipt',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]