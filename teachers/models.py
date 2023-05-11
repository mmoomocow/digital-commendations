from django.db import models

# Create your models here.


class Teacher(models.Model):
    """
    The model for teachers and staff.

    This model contains data that is specific to teachers and staff, and therefore not suitable for the
    generic user model. To access generic data, use the user reverse relation.

    Related Models:
        :model:`commendation.Commendation` - Commendations are linked to teachers when

        :model:`users.User` - The user model that is linked to the teacher

    Fields:
        * id (AutoField): The primary key of the teacher
        * staff_code (str): The staff code of the teacher
        * user (ForeignKey): The user model that is linked to the teacher
        * house_group (str): The house group the teacher is a member of
        * user (ForeignKey): Reverse relation to the user model

        Docs updated on: 30/7/2022
    """

    # Teacher ID
    # Used internally to uniquely identify teachers
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="ID",
    )

    # Staff code
    # Uniquely identifies the teacher (can be repeated once a teacher has left)
    staff_code = models.CharField(
        max_length=2, unique=True, blank=True, default="", verbose_name="Staff Code"
    )

    # House group
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
        default="",
        verbose_name="House Group",
    )

    # Is management
    # Whether the teacher is a management teacher who can see all students and commendations
    is_management = models.BooleanField(default=False, verbose_name="Is Management")

    class Meta:
        """Meta settings for model"""

        ordering = ("staff_code",)

    def __str__(self) -> str:
        if not hasattr(self, "user"):
            return f"{self.staff_code}"
        return f"{self.staff_code} ({self.user.first_name} {self.user.last_name})"
