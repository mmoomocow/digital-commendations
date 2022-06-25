# Generated by Django 4.0.4 on 2022-05-24 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("students", "0002_student_caregiver_student_house_group_and_more"),
        ("teachers", "0002_alter_teacher_options_teacher_house_group_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="commendation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID",
                    ),
                ),
                (
                    "commendation_type",
                    models.CharField(
                        choices=[
                            ("R", "Respect"),
                            ("I", "Integrity"),
                            ("S", "Service"),
                            ("E", "Excellence"),
                            ("O", "Other"),
                        ],
                        max_length=1,
                        verbose_name="Commendation Type",
                    ),
                ),
                ("reason", models.CharField(max_length=200, verbose_name="Reason")),
                ("date_time", models.DateTimeField(verbose_name="Date and Time given")),
                (
                    "students",
                    models.ManyToManyField(
                        to="students.student", verbose_name="Students"
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="teachers.teacher",
                        verbose_name="Teacher",
                    ),
                ),
            ],
        ),
    ]
