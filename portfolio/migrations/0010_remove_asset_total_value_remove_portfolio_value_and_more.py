# Generated by Django 5.1.5 on 2025-02-06 03:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_snapshot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='total_value',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='value',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='total_value',
        ),
        migrations.AddField(
            model_name='league',
            name='num_portfolios',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
