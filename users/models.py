from django.db import models
from django.contrib.auth.models import AbstractBaseUser as defaultUser
from django.contrib.auth.models import BaseUserManager as defaultUserManager
from django.contrib.auth.models import PermissionsMixin as defaultPermissionsMixin

# Create your models here.


class UserManager(defaultUserManager):
    """Manager for the User model."""

    def create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str = None,
    ):
        """
        Create a new user

        Args:
            username (str): The username that the user will use to login
            email (str): The email address of the user
            first_name (str): The user's first name
            last_name (str): The user's last name
            password (str): The password of the user that will be salted and hashes. Defaults to None.

        Raises:
            ValueError: Users must have a username
            ValueError: Users must have an email

        Returns:
            User: Returns the newly created user
        """

        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        """
        Create a new user with superuser privileges

        Args:
            username (str): The username that the user will use to login
            email (str): The email address of the user
            first_name (str): The user's first name
            last_name (str): The user's last name
            password (str): The password of the user that will be salted and hashes. Defaults to None.

        Returns:
            User: Returns the newly created user
        """
        user = self.create_user(
            username, email, first_name, last_name, password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(defaultUser, defaultPermissionsMixin):
    """
    The default, generic user object that exists as a base for all users
    in the system.
    This is also the user object that is used to authenticate users, as doing
    authentication for students, teachers, and caregivers would require far
    more code maintenance than just adding a new user object.
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
