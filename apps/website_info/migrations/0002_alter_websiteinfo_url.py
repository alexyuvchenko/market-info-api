# Generated by Django 5.1.7 on 2025-03-09 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website_info", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="websiteinfo",
            name="url",
            field=models.URLField(max_length=2048, unique=True),
        ),
    ]
