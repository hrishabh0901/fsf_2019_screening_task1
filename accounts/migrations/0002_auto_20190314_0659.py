# Generated by Django 2.1.7 on 2019-03-14 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='team.Team'),
        ),
    ]
