# Generated by Django 4.1.7 on 2023-10-18 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0017_remove_customer_locality"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderplaced",
            name="status",
            field=models.CharField(
                choices=[
                    ("Placed", "Placed"),
                    ("Accepted", "Accepted"),
                    ("Shipped", "Shipped"),
                    ("Delivered", "Delivered"),
                    ("Cancel", "Cancel"),
                ],
                default="orderd_date",
                max_length=100,
            ),
        ),
    ]