# Generated by Django 4.2.17 on 2025-01-20 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_league_num_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfolio')),
            ],
        ),
    ]
