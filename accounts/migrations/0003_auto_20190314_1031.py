# Generated by Django 2.1.7 on 2019-03-14 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190314_0659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='team',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='team.Team'),
        ),
    ]
