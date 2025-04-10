# Generated by Django 5.1.6 on 2025-04-01 02:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_alter_asset_quantity_alter_transaction_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asset',
            name='previous_close',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portfolio',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
