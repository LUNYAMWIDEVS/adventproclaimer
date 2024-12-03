# Generated by Django 4.2.13 on 2024-11-07 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evangelism', '0008_alter_bibleworkerdailyreport_interest_phone_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicalmissionarydailyreport',
            old_name='homes_visited',
            new_name='new_patient_number',
        ),
        migrations.RenameField(
            model_name='medicalmissionarydailyreport',
            old_name='studies_given',
            new_name='number_of_patients',
        ),
        migrations.RenameField(
            model_name='medicalmissionarydailyreport',
            old_name='date_posted',
            new_name='timestamp',
        ),
        migrations.RemoveField(
            model_name='medicalmissionarydailyreport',
            name='content',
        ),
        migrations.RemoveField(
            model_name='medicalmissionarydailyreport',
            name='email',
        ),
        migrations.RemoveField(
            model_name='medicalmissionarydailyreport',
            name='name',
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='challenges_missionary_side',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='check_on_the_following_areas',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='description_on_parameters',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='drink',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='fill_in_the_following_no',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='fill_in_the_following_no1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='fill_in_the_following_row3',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='fill_in_the_following_yes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='fill_in_the_following_yes1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='food',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='fruits',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='health_counseling_shared',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='health_history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='herb',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='hospital_referrals_summary',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='hydotherapies_administered',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='interventions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='juices',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='legumes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='massage',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='measure',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='missionary_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='name_of_patient',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='name_of_patients',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='needs_interest_side',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='number_of_hours',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='nurture_rp_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='nurture_rp_phone_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='nuts',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='open_air_hours',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='patient_contact_phone_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='physiotherapies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='quality_perspective',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='seeds',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='signs_and_symptoms',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='symptoms_that_are_better',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='symptoms_that_have_worsened',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='vegetables',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='vital_signs_heart_rate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='vital_signs_respiratory_rate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='vital_signs_temperature',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='walk_distance_minutes',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='water_quantify',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='wholegrains',
            field=models.TextField(blank=True, null=True),
        ),
    ]