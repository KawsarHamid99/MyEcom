# Generated by Django 4.1.7 on 2023-10-26 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_myproductlist"),
    ]

    operations = [
        migrations.RenameModel(old_name="MYProductList", new_name="StateList",),
    ]
