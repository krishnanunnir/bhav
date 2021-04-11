# Generated by Django 3.1.7 on 2021-04-11 16:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='importdate',
            old_name='CLOSE',
            new_name='close_value',
        ),
        migrations.RenameField(
            model_name='importdate',
            old_name='CODE',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='importdate',
            old_name='HIGH',
            new_name='high_value',
        ),
        migrations.RenameField(
            model_name='importdate',
            old_name='LOW',
            new_name='low_value',
        ),
        migrations.RenameField(
            model_name='importdate',
            old_name='NAME',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='importdate',
            old_name='OPEN',
            new_name='open_value',
        ),
        migrations.RemoveField(
            model_name='importdetails',
            name='imported_on',
        ),
        migrations.AddField(
            model_name='importdate',
            name='imported_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='importdetails',
            name='imported_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='importdetails',
            name='status',
            field=models.IntegerField(choices=[(1, 'SUCCESS'), (0, 'FAILURE')], default=0),
        ),
    ]
