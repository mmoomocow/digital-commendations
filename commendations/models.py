from django.db import models

# Create your models here.


class commendation(models.Model):
    """
    The model for commendations.

    This model stores data for the commendations that have been awarded to students by teachers.

    Related Models:
        * :model:`users.User` - The user model that is linked to the Student/Teacher
        * :model:`teachers.Teacher` - The teacher model that is linked to the Teacher that awarded the commendation
        * :model:`students.Student` - The student model that is linked to the Student that was awarded the commendation

    Fields:
        * id (AutoField): The primary key of the commendation
        * commendation_type (str): The type of commendation that was awarded
        * reason (str): The reason for the commendation
        * date_time (DateTimeField): The date and time the commendation was awarded
        * teacher (ForeignKey): The teacher model that is linked to the Teacher that awarded the commendation
        * student (ManyToManyField): The student model that is linked to the Student that was awarded the commendation

    Docs updated on: 30/7/2022
    """

    # Unique id for commendations
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="ID",
    )

    # The type of commendation given
    RESPECT = "R"
    INTEGRITY = "I"
    SERVICE = "S"
    EXCELLENCE = "E"
    OTHER = "O"
    COMMENDATION_TYPE_CHOICES = (
        (RESPECT, "Respect"),
        (INTEGRITY, "Integrity"),
        (SERVICE, "Service"),
        (EXCELLENCE, "Excellence"),
        (OTHER, "Other"),
    )
    commendation_type = models.CharField(
        max_length=1,
        choices=COMMENDATION_TYPE_CHOICES,
        blank=False,
        null=False,
        verbose_name="Commendation Type",
    )

    # The reason for giving the commendation
    reason = models.TextField(
        max_length=500, blank=False, null=False, verbose_name="Reason"
    )

    # The date and time the commendation was given
    date_time = models.DateTimeField(
        blank=False, null=False, verbose_name="Date and Time given", auto_now_add=True
    )

    # The teacher who gave the commendation
    teacher = models.ForeignKey(
        "teachers.teacher",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Teacher",
    )

    # The student(s) who received the commendation
    students = models.ManyToManyField(
        "students.student", blank=False, verbose_name="Students"
    )

    class Meta:
        """Meta settings for model"""

        verbose_name = "Commendation"
        verbose_name_plural = "Commendations"

    def __str__(self) -> str:
        return f"Commendation ID: {self.id}"
