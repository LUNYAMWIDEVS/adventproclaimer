# Generated by Django 4.2.13 on 2024-09-08 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evangelism', '0004_remove_survey_scheduled_date_survey_scheduled_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
