# Generated by Django 2.1.7 on 2019-03-14 12:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0008_auto_20190314_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='members',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('user1', 'user1'), ('user3', 'user3'), ('user4', 'user4'), ('user2', 'user2'), ('user5', 'user5'), ('hrishabh901', 'hrishabh901')], max_length=40), default=None, null=True, size=None),
        ),
    ]