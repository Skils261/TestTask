# Generated by Django 4.1 on 2023-05-04 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_customuser_username"),
    ]

    operations = [
        migrations.RemoveField(model_name="customuser", name="username",),
    ]
