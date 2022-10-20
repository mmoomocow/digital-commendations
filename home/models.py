from django.db import models

# Create your models here.


class Contact(models.Model):
    """Model for the contact page, where users can send messages to the website owner."""

    # Basic contact information
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    subject = models.CharField(max_length=100, blank=False, null=False)
    message = models.TextField(blank=False, null=False)

    # Status
    DONE = "Done"
    REPLIED = "Replied"
    NOT_REPLIED = "Not Replied"
    STATUS_CHOICES = (
        (DONE, "Done"),
        (REPLIED, "Replied"),
        (NOT_REPLIED, "Not Replied"),
    )

    status = models.TextField(
        max_length=20, choices=STATUS_CHOICES, default=NOT_REPLIED
    )

    def __str__(self) -> str:
        """Return the name of the contact."""
        return self.subject

    class Meta:
        """Meta settings for the contact model."""

        verbose_name = "Contact"
        verbose_name_plural = "Contact Requests"
