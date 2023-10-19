# Generated by Django 4.1.7 on 2023-10-19 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0019_productcolor_productsize_product_color_product_size"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="color",
            field=models.ManyToManyField(blank=True, to="app.productcolor"),
        ),
        migrations.AlterField(
            model_name="product",
            name="size",
            field=models.ManyToManyField(blank=True, to="app.productsize"),
        ),
    ]
