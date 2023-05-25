from django.test import TestCase

from commendationSite import testHelper

from .admin import ContactAdmin
from .models import Contact

# Create your tests here.


class TestHomePages(TestCase):
    def test_index_teacher(self):
        teacher = testHelper.createTeacher(self, is_management=False)
        self.client.force_login(teacher)
        response = self.client.get("/")
        self.assertRedirects(response, "/commendations/award/")

    def test_contact_page(self):
        testHelper.get_page(self, "/contact/", "home/contact.html")

    def test_contact_page_post(self):
        testHelper.post_page(
            self,
            "/contact/",
            data={
                "name": "Test",
                "email": "test@example.com",
                "subject": "Test",
                "message": "Test",
            },
            status_code=201,
        )

        # Test that it was created
        self.assertEqual(
            Contact.objects.count(), 1, "Contact was not created from post request"
        )

    def test_about_page(self):
        testHelper.get_page(self, "/about/", "home/about.html")

    def test_privacy_page(self):
        testHelper.get_page(self, "/privacy/", "home/privacy.html")


class TestContactModel(TestCase):
    def setUp(self) -> None:
        self.contact = Contact(
            name="Test Name",
            email="test@example.com",
            subject="Test Subject",
            message="Test Message",
        )
        self.contact.save()
        self.contact2 = Contact(
            name="Test Name 2",
            email="test@example.com",
            subject="Test Subject 2",
            message="Test Message 2",
        )
        self.contact2.save()

    def test_contact_model(self):
        self.assertEqual(self.contact.name, "Test Name")
        self.assertEqual(self.contact.email, "test@example.com")
        self.assertEqual(self.contact.subject, "Test Subject")
        self.assertEqual(self.contact.message, "Test Message")

    def test_contact_str(self):
        self.assertEqual(str(self.contact), "Test Subject")

    def test_contact_admin_actions(self):
        # Make a queryset of the contacts
        queryset = Contact.objects.all()
        # Mark the messages as replied
        ContactAdmin.mark_as_replied(ContactAdmin, None, queryset)
        # Check that the status has been updated
        self.assertEqual(Contact.objects.get(pk=1).status, Contact.REPLIED)

        ContactAdmin.mark_as_done(ContactAdmin, None, queryset)
        self.assertEqual(Contact.objects.get(pk=1).status, Contact.DONE)
        ContactAdmin.mark_as_not_replied(ContactAdmin, None, queryset)
        self.assertEqual(Contact.objects.get(pk=1).status, Contact.NOT_REPLIED)
