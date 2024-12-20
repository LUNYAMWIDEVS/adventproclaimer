# Generated by Django 4.2.13 on 2024-09-08 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evangelism', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdventistMuslimRelationsDailyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='bibleworkerdailyreport',
            name='title',
        ),
        migrations.RemoveField(
            model_name='medicalmissionarydailyreport',
            name='title',
        ),
        migrations.AddField(
            model_name='bibleworkerdailyreport',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='bibleworkerdailyreport',
            name='homes_visited',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bibleworkerdailyreport',
            name='name',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='bibleworkerdailyreport',
            name='studies_given',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalmissionarydailyreport',
            name='name',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1024, null=True)),
                ('scheduled_date', models.DateTimeField(blank=True, null=True)),
                ('scheduled_time', models.TimeField(blank=True, null=True)),
                ('interest_type', models.CharField(blank=True, max_length=100, null=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('adventist_muslim_relations', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evangelism.adventistmuslimrelationsdailyreport')),
                ('bible_worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evangelism.bibleworkerdailyreport')),
                ('medical_missionary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evangelism.medicalmissionarydailyreport')),
            ],
        ),
    ]
