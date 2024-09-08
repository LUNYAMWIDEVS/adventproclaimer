# Generated by Django 4.2.13 on 2024-09-08 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evangelism', '0002_adventistmuslimrelationsdailyreport_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='interest_type',
            field=models.CharField(blank=True, choices=[('Bible Worker', 'Bible Worker'), ('Medical Missionary', 'Medical Missionary'), ('Adentist Muslim Relations', 'Adentist Muslim Relations')], default='Bible Worker', max_length=100, null=True),
        ),
    ]
