# Generated by Django 4.0.6 on 2022-08-01 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0003_alter_teacher_house_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='is_management',
            field=models.BooleanField(default=False, verbose_name='Is Management'),
        ),
    ]
