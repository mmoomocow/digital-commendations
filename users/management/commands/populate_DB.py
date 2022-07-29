from random import choice
from faker import Faker
from faker.providers import profile as fake_profile
from faker.providers import misc as fake_misc
from users import models as user_models
from students import models as student_models
from teachers import models as teacher_models
from django.core.management.base import BaseCommand

fake = Faker()
fake.add_provider(fake_profile)
fake.add_provider(fake_misc)


def generate_teacher(number):
    teacher_houses = [
        teacher_models.Teacher.ANDERSON,
        teacher_models.Teacher.BEGG,
        teacher_models.Teacher.HERRON,
        teacher_models.Teacher.ROSS,
        teacher_models.Teacher.SOMERVILLE,
    ]
    for _ in range(number):
        # Generate a profile for the dummy teacher
        profile = fake.simple_profile()
        # Create the dummy user object
        user = user_models.User.objects.create_user(
            username=profile["username"],
            password=fake.password(length=12),
            first_name=profile["name"].split(" ")[0],
            last_name=profile["name"].split(" ")[1],
            email=profile["mail"],
        )
        user.is_teacher = True
        user.teacher = teacher_models.Teacher.objects.create(
            staff_code=fake.unique.lexify(text="??"),
            house_group=choice(teacher_houses),
        )
        user.save()


def generate_student(number):
    student_houses = [
        student_models.Student.ANDERSON,
        student_models.Student.BEGG,
        student_models.Student.HERRON,
        student_models.Student.ROSS,
        student_models.Student.SOMERVILLE,
    ]
    for _ in range(number):
        # Generate a profile for the dummy student
        profile = fake.simple_profile()
        # Create the dummy user object
        user = user_models.User.objects.create_user(
            username=profile["username"],
            password=fake.password(length=12),
            first_name=profile["name"].split(" ")[0],
            last_name=profile["name"].split(" ")[1],
            email=profile["mail"],
        )
        user.is_student = True
        user.student = student_models.Student.objects.create(
            id=fake.unique.numerify(text="#####"),
            tutor_room=fake.lexify(text="???"),
            house_group=choice(student_houses),
            year_level=fake.random_int(min=9, max=13),
        )
        user.save()


class Command(BaseCommand):
    """
    Populate the database with dummy data
    """

    help = "Populates the database with dummy data."

    def add_arguments(self, parser):
        parser.add_argument("teachers", nargs="+", type=int)
        parser.add_argument("students", nargs="+", type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Populating the database..."))

        self.stdout.write(
            self.style.NOTICE(f"Creating {options['teachers'][0]} teachers...")
        )
        generate_teacher(options["teachers"][0])
        self.stdout.write(self.style.SUCCESS("Done!\n\n"))

        self.stdout.write(
            self.style.NOTICE(f"Creating {options['students'][0]} students...")
        )
        generate_student(options["students"][0])
        self.stdout.write(self.style.SUCCESS("Done!\n\n"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully generated {options['teachers'][0] + options['students'][0]} users"
            )
        )
