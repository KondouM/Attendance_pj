# Generated by Django 5.0.6 on 2024-06-21 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendances",
            name="work_duration",
            field=models.DurationField(blank=True, null=True),
        ),
    ]
