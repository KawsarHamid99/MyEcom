# Generated by Django 4.1.7 on 2023-09-16 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_alter_brand_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="category",
            field=models.ManyToManyField(blank=True, to="app.category"),
        ),
        migrations.AlterField(
            model_name="brand",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="brand"),
        ),
    ]
