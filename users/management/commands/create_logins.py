# Django management command to create users

from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import misc as fake_misc
from faker.providers import profile as fake_profile

from students import models as student_models
from teachers import models as teacher_models
from users import models as user_models


class Command(BaseCommand):
    help = "Create users"

    def handle(self, *args, **options):
        # Create a super user that is a teacher and management, a student, and a caregiver

        # Create a super user
        superUser = user_models.User.objects.create(
            username="teacher",
            first_name="James",
            last_name="Robinson",
            email="superuser@example.com",
        )
        superUser.is_superuser = True
        superUser.is_staff = True
        superUser.is_teacher = True
        superUser.set_password("password")
        superUser.save()

        superUser_teacher = teacher_models.Teacher.objects.create(
            staff_code="SU",
            house_group=teacher_models.Teacher.ANDERSON,
        )
        superUser.teacher = superUser_teacher
        superUser.save()

        print("Created super user, username: teacher, password: password")

        # Create 2 students
        student = user_models.User.objects.create(
            username="student",
            first_name="Ethan",
            last_name="Nelson",
            email="student@example.com",
        )
        student.is_student = True
        student.set_password("password")
        student.save()

        student_student = student_models.Student.objects.create(
            id=12345,
            tutor_room="AHb",
            house_group=student_models.Student.ANDERSON,
        )
        student.student = student_student
        student.save()

        print("Created student, username: student, password: password")

        student2 = user_models.User.objects.create(
            username="student2",
            first_name="Joshua",
            last_name="Nelson",
            email="student2@example.com",
        )
        student2.is_student = True
        student2.set_password("password")
        student2.save()

        student2_student = student_models.Student.objects.create(
            id=23456,
            tutor_room="AHb",
            house_group=student_models.Student.ANDERSON,
        )
        student2.student = student2_student
        student2.save()

        print("Created student, username: student2, password: password")

        # Create a caregiver
        caregiver = user_models.User.objects.create(
            username="caregiver",
            first_name="Harry",
            last_name="Nelson",
            email="caregiver@example.com",
        )
        caregiver.is_caregiver = True
        caregiver.set_password("password")
        caregiver.save()

        caregiver_caregiver = student_models.Caregiver.objects.create()
        caregiver_caregiver.students.add(student_student)
        caregiver_caregiver.students.add(student2_student)
        caregiver.caregiver = caregiver_caregiver
        caregiver.save()

        print("Created caregiver, username: caregiver, password: password")
