# Generated by Django 4.2 on 2024-01-11 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moneytracker', '0008_performance_last_time_sendend_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='last_time_sendend',
            new_name='last_time_sent',
        ),
    ]
