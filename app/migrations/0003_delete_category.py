# Generated by Django 4.1.7 on 2023-09-14 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_category"),
    ]

    operations = [
        migrations.DeleteModel(name="Category",),
    ]
