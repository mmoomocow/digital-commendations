# Generated by Django 4.0.6 on 2022-08-12 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_alter_student_house_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='next_milestone',
            field=models.IntegerField(blank=True, choices=[(25, "Dean's Certificate"), (50, 'Green Jr School spirit badge'), (100, 'Blue Jr School spirit badge'), (150, 'Gold Jr School spirit badge')], null=True, verbose_name='Next Milestone'),
        ),
    ]
