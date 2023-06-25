from __future__ import annotations

from typing import Optional

from django.contrib import messages
from django.contrib.auth.models import AbstractBaseUser as defaultUser
from django.contrib.auth.models import PermissionsMixin as defaultPermissionsMixin
from django.contrib.auth.models import UserManager as defaultUserManager
from django.db import models
from django.http.request import HttpRequest

# Create your models here.


class UserManager(defaultUserManager):
    """Manager for the User model. Currently no modifications."""


class User(defaultUser, defaultPermissionsMixin):
    """
    The default, generic user object that exists as a base for all users
    in the system.

    It extends Django's defaultUser object and defaultPermissionsMixin object.

    Related Models:
        * :model:`teachers.Teacher` - The teacher model that is linked to the user
        * :model:`students.Student` - The student model that is linked to the user
        * :model:`students.Caregiver` - The caregiver model that is linked to the user

    Fields:
        * id (AutoField): The primary key of the user
        * username (str): The username that the user will use to login
        * password (str): The password of the user that will be salted and hashes. Defaults to None.
        * email (str): The email address of the user
        * first_name (str): The user's first name
        * last_name (str): The user's last name
        * is_active (bool): Whether the user is active or not
        * is_staff (bool): Whether the user is a staff member or not
        * is_superuser (bool): Whether the user is a superuser or not
        * date_joined (DateTimeField): The date and time the user joined the system
        * last_login (DateTimeField): The date and time the user last logged in
        * is_teacher (bool): Whether the user is a teacher or not
        * is_student (bool): Whether the user is a student or not
        * is_caregiver (bool): Whether the user is a caregiver or not
        * teacher (ForeignKey): The teacher model that is linked to the user
        * student (ForeignKey): The student model that is linked to the user
        * caregiver (ForeignKey): The caregiver model that is linked to the user

    Methods:
        * delete(): Delete the user and any linked models of teachers, students and caregivers

    Docs updated on: 30/7/2022
    """

    # Custom user manager
    objects = UserManager()
    # Required fields for user
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    # User ID
    # This field is just here to internally identify and link to the user
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="ID",
    )

    # ------ BASIC USER INFORMATION ------ #
    # Email Address
    email = models.EmailField(
        unique=True, blank=False, null=False, verbose_name="Email Address"
    )
    # Username
    # This is what the user will use to log in
    username = models.CharField(
        max_length=30, unique=True, blank=False, null=False, verbose_name="Username"
    )
    # Password
    password = models.CharField(
        max_length=128, blank=False, null=False, verbose_name="Password"
    )
    # Title
    title = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="Title"
    )
    # First Name
    first_name = models.CharField(
        max_length=128, blank=False, null=False, verbose_name="First Name"
    )
    # Last Name
    last_name = models.CharField(
        max_length=128, blank=False, null=False, verbose_name="Last Name"
    )
    # User's last login time
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Last Login")

    # ------ USER ACCESS LEVELS ------ #
    # Can log in to django's backend administration site, not reflective of
    # staff status within the school
    is_staff = models.BooleanField(default=False)
    # User is a superuser, can access the django admin site with all permissions
    is_superuser = models.BooleanField(default=False)
    # User is active and can log in
    is_active = models.BooleanField(default=True)

    # ------ USER LINKS ------ #
    # Is the user a teacher, student or caregiver?
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_caregiver = models.BooleanField(default=False)

    # Link to the teacher, student or caregiver
    teacher = models.OneToOneField(
        "teachers.Teacher", on_delete=models.CASCADE, null=True, blank=True
    )
    student = models.OneToOneField(
        "students.Student", on_delete=models.CASCADE, null=True, blank=True
    )
    caregiver = models.OneToOneField(
        "students.Caregiver", on_delete=models.CASCADE, null=True, blank=True
    )

    USERNAME_FIELD = "username"

    class Meta:
        """Meta settings for model"""

        ordering = ("id",)
        verbose_name = "User"
        verbose_name_plural = "Users"

    # When the object is displayed in string format, display the user's name
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # When the user is deleted, delete the user's teacher, student or caregiver
    def delete(self, *args, **kwargs):
        """Delete the user and any linked models of teachers, students and caregivers"""
        if self.is_teacher:
            self.teacher.delete()
        elif self.is_student:
            self.student.delete()
        elif self.is_caregiver:
            self.caregiver.delete()
        super().delete(*args, **kwargs)

    def can_login(self, *args, request: Optional[HttpRequest] = None, **kwargs):
        """Check if a user can login."""
        if not self.is_active:
            if request:
                messages.error(
                    request, "Your account is not active, please contact support."
                )
            return False
        if not self.is_teacher and not self.is_superuser:
            if request:
                messages.error(
                    request, "Sorry, only teachers can log in currently for now :("
                )
            return False
        if request:
            messages.success(
                request,
                f"You have successfully logged in! Welcome back {self.first_name}",
            )
        return True
