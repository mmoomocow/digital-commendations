# Generated by Django 4.0.6 on 2022-09-22 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_contact_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Contact', 'verbose_name_plural': 'Contact Requests'},
        ),
    ]