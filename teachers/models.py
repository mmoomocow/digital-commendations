from django.db import models

# Create your models here.


class Teacher(models.Model):
    """
    The model for teachers and staff.

    This model will link to commendations, and contain data that is
    specific to staff members only, and therefore not suitable for the
    generic user model.

    The generic user model contains all of the basic information that
    is required for a user to log in, and contains email address, name
    password etc, so this information should not be stored in the teacher model
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
        max_length=2, unique=True, blank=True, null=True, verbose_name="Staff Code"
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
        null=True,
        verbose_name="House Group",
    )

    class Meta:
        """Meta settings for model"""

        ordering = ("staff_code",)

    def __str__(self) -> str:
        if not hasattr(self, "user"):
            return f"{self.staff_code}"
        return f"{self.staff_code} ({self.user.first_name} {self.user.last_name})"
