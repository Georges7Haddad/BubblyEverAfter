# Generated by Django 3.0.3 on 2020-04-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("MembershipApp", "0002_contact"),
    ]

    operations = [
        migrations.CreateModel(
            name="bubblyevents",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=127)),
                ("location", models.CharField(max_length=127)),
                ("schedule", models.CharField(max_length=127)),
                ("description", models.CharField(max_length=1023)),
            ],
        ),
        migrations.RenameField(
            model_name="contact", old_name="adjectives", new_name="Please_tell_us_3_adjectives_that_describe_you_most",
        ),
        migrations.RenameField(
            model_name="contact", old_name="collab", new_name="how_can_we_collaborate_and_get_to_know_you_better",
        ),
        migrations.RenameField(model_name="contact", old_name="socialmedia", new_name="social_media", ),
        migrations.AlterField(model_name="contact", name="email", field=models.EmailField(max_length=127), ),
    ]
