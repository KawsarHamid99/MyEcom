# Generated by Django 4.1.7 on 2023-10-17 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0014_orderplaced_address_orderplaced_orderid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderplaced",
            name="price_per_unit",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
