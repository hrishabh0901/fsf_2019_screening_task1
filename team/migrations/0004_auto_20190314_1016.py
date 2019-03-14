# Generated by Django 2.1.7 on 2019-03-14 10:16

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_auto_20190314_0659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='members',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('user1', 'user1'), ('user2', 'user2'), ('user3', 'user3'), ('user4', 'user4'), ('user5', 'user5'), ('hrishabh901', 'hrishabh901')], max_length=40), size=None),
        ),
    ]
