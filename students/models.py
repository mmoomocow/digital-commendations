from django.db import models

# Create your models here.


class Caregiver(models.Model):
    pass


class Student(models.Model):
    """
    The model for students.

    This model will link to commendations, and contain data that is
    specific to students only, and therefore not suitable for the
    generic user model.
    """

    # The KAMAR assigned student ID is a unique identifier for the student
    id = models.IntegerField(
        unique=True,
        primary_key=True,
        blank=False,
        null=False,
        verbose_name="Student ID",
    )

    # The student's tutor room
    tutor_room = models.CharField(
        max_length=3, blank=True, null=True, verbose_name="Tutor Room"
    )
    # The student's house group
    ANDERSON = "A"
    BEGG = "B"
    ROSS = "R"
    HERRON = "H"
    SOMERVILLE = "S"
    HOUSE_GROUP_CHOICES = (
        (ANDERSON, "Anderson"),
        (BEGG, "Begg"),
        (ROSS, "Ross"),
        (HERRON, "Herron"),
        (SOMERVILLE, "Somerville"),
    )
    house_group = models.CharField(
        max_length=20,
        choices=HOUSE_GROUP_CHOICES,
        blank=True,
        null=True,
        verbose_name="House Group",
    )
    # The student's year level
    YEAR9 = 9
    YEAR10 = 10
    YEAR11 = 11
    YEAR12 = 12
    YEAR13 = 13
    YEAR_LEVEL_CHOICES = (
        (YEAR9, "Year 9"),
        (YEAR10, "Year 10"),
        (YEAR11, "Year 11"),
        (YEAR12, "Year 12"),
        (YEAR13, "Year 13"),
    )
    year_level = models.IntegerField(
        choices=YEAR_LEVEL_CHOICES, blank=True, null=True, verbose_name="Year Level"
    )

    # Parent/caregiver
    caregiver = models.ForeignKey(
        Caregiver,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Caregiver",
    )

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        try:
            return str(f"{self.user.first_name} {self.user.last_name} ({self.id})")
        except:
            return str(f"{self.id}")
