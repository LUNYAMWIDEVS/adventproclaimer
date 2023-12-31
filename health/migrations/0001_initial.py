# Generated by Django 4.0.4 on 2023-11-13 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('disease', models.CharField(max_length=255)),
                ('symptoms', models.TextField()),
                ('causes', models.TextField()),
                ('hydro', models.TextField()),
                ('treatments', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='health.disease')),
            ],
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='health.disease')),
            ],
        ),
        migrations.CreateModel(
            name='HydroTherapy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='health.disease')),
            ],
        ),
        migrations.CreateModel(
            name='Cause',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='health.disease')),
            ],
        ),
    ]
