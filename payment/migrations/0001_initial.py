# Generated by Django 4.0.4 on 2024-03-07 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(db_index=True, max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('status', models.CharField(choices=[('O', 'Ok'), ('P', 'Pending'), ('C', 'Cancelled')], default='P', max_length=1)),
                ('business_short_code', models.CharField(blank=True, max_length=20, null=True)),
                ('ref_number', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
    ]
