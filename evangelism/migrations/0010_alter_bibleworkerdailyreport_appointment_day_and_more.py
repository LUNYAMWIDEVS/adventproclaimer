# Generated by Django 4.2.13 on 2024-12-03 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evangelism', '0009_rename_homes_visited_medicalmissionarydailyreport_new_patient_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='appointment_day',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='appointment_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='appointments',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='challenges',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='home_visited',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='homes_rejected',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='homes_under_appointments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='homes_visited',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='interest_phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='missionary_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='needs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='nurturing_rp_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='nurturing_rp_phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='people_attended',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='prayer_requests',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='study',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bibleworkerdailyreport',
            name='to_be_nurtured',
            field=models.BooleanField(default=False),
        ),
    ]
