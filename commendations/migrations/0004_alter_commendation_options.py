# Generated by Django 4.0.6 on 2022-07-30 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commendations', '0003_alter_commendation_date_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commendation',
            options={'verbose_name': 'Commendation', 'verbose_name_plural': 'Commendations'},
        ),
    ]