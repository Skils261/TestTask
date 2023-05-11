# Generated by Django 4.1 on 2023-05-04 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0001_initial"),
        ("accounts", "0004_remove_customuser_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="organization",
            field=models.ManyToManyField(
                related_name="user_organization", to="general.organization"
            ),
        ),
    ]
