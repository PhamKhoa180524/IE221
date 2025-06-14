# Generated by Django 5.2.1 on 2025-05-28 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0008_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='check_in',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='check_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.room'),
        ),
        migrations.AddField(
            model_name='cart',
            name='type',
            field=models.CharField(choices=[('SERVICE', 'Service'), ('ROOM', 'Room')], default='SERVICE', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.service'),
        ),
    ]
