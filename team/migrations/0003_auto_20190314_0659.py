# Generated by Django 2.1.7 on 2019-03-14 06:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_auto_20190314_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='members',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('user2', 'user2'), ('user1', 'user1'), ('user4', 'user4'), ('user5', 'user5'), ('user3', 'user3'), ('hrishabh0901', 'hrishabh0901')], max_length=10), size=None),
        ),
    ]
