# Generated by Django 5.1.2 on 2024-12-16 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_servicebooking_time_call'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='payment_status',
        ),
    ]
