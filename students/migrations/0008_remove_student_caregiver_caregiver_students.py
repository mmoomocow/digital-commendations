# Generated by Django 4.2.1 on 2023-07-05 21:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0007_alter_student_house_group_alter_student_tutor_room"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="caregiver",
        ),
        migrations.AddField(
            model_name="caregiver",
            name="students",
            field=models.ManyToManyField(blank=True, to="students.student"),
        ),
    ]
