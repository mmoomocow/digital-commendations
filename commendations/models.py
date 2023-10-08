from django.db import models

# Create your models here.


class Commendation(models.Model):
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

    # Inside/outside of classroom
    INSIDE = "I"
    OUTSIDE = "O"
    EXTRACURRICULAR = "E"
    INSIDE_OUTSIDE_CHOICES = (
        (INSIDE, "In class"),
        (OUTSIDE, "Out of class"),
        (EXTRACURRICULAR, "Extracurricular"),
    )
    inside_outside = models.CharField(
        max_length=1,
        choices=INSIDE_OUTSIDE_CHOICES,
        blank=False,
        null=False,
        default=INSIDE,
        verbose_name="Commendation Location",
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


class Milestone(models.Model):
    """
    The model for commendation Milestones.

    This model stores data for the milestones for numbers of commendations awarded to students.

    Related Models:
        * :model:`users.User` - The user model that is linked to the Student/Teacher
        * :model:`students.Student` - The student model of the student who received the milestone award

    Fields:
        * id (AutoField): The primary key of the commendation
        * milestone_type (int): The type of commendation that was awarded - based on the number of commendations given
        * date_time (DateTimeField): The date and time the commendation was awarded
        * student (ForeignKey): The student who received the milestone award

    Docs updated on: 12/8/2022
    """

    # Unique id for milestones
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="ID",
    )

    # The type of milestone
    CERTIFICATE = 25
    GREEN = 50
    BLUE = 100
    GOLD = 150
    MILESTONE_TYPE_CHOICES = (
        (CERTIFICATE, f"Dean's Certificate for {CERTIFICATE} commendations"),
        (GREEN, f"Green Jr School spirit badge for {GREEN} commendations"),
        (BLUE, f"Blue Jr School spirit badge for {BLUE} commendations"),
        (GOLD, f"Gold Jr School spirit badge for {GOLD} commendations"),
    )
    milestone_type = models.IntegerField(
        choices=MILESTONE_TYPE_CHOICES,
        blank=False,
        null=False,
        verbose_name="Milestone Type",
    )

    # The date and time the milestone was given
    date_time = models.DateTimeField(
        blank=False, null=False, verbose_name="Date and Time given", auto_now_add=True
    )

    # The student(s) who received the milestone
    student = models.ForeignKey(
        "students.student",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Student",
    )

    # Has the milestone been awarded?
    awarded = models.BooleanField(
        default=False, blank=False, null=False, verbose_name="Awarded"
    )

    class Meta:
        """Meta settings for model"""

        verbose_name = "Milestone"
        verbose_name_plural = "Milestones"

    def __str__(self) -> str:
        milestone_type = [
            choice[1]
            for choice in Milestone.MILESTONE_TYPE_CHOICES
            if choice[0] == self.milestone_type
        ][0]
        return f"{milestone_type} - {self.student}"

    def prettyPrint(self) -> str:
        """Pretty print the milestone type."""
        milestone_type = [
            choice[1]
            for choice in Milestone.MILESTONE_TYPE_CHOICES
            if choice[0] == self.milestone_type
        ][0]
        return milestone_type
