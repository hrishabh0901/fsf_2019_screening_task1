# Generated by Django 2.1.7 on 2019-03-16 20:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0014_auto_20190315_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='members',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('user7', 'user7'), ('user1', 'user1'), ('user9', 'user9'), ('user3', 'user3'), ('user11', 'user11'), ('user5', 'user5'), ('user4', 'user4'), ('user10', 'user10'), ('user12', 'user12'), ('user13', 'user13'), ('user8', 'user8'), ('user6', 'user6'), ('user2', 'user2'), ('Rangeela@deewana', 'Rangeela@deewana'), ('user14', 'user14'), ('hrishabh901', 'hrishabh901')], max_length=40), default=None, null=True, size=None),
        ),
    ]