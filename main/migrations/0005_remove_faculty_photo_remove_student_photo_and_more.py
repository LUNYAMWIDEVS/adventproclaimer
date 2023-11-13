# Generated by Django 4.0.4 on 2023-01-23 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_material_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='student',
            name='photo',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='file',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='file',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
