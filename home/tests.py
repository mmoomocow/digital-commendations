from django.test import TestCase

from commendationSite import testHelper

from .admin import ContactAdmin
from .models import Contact

# Create your tests here.


class TestHomePages(TestCase):
    def setUp(self):
        self.user = testHelper.createUser(self)
        self.teacher = testHelper.createTeacher(self)
        self.student = testHelper.createStudent(self)
        self.caregiver = testHelper.createCaregiver(self)
        self.superuser = testHelper.createUser(self, is_superuser=True)

    def test_index_page(self):
        testHelper.get_page(self, "/", "home/index.html")

    def test_portal_teacher(self):
        self.client.force_login(self.teacher)
        testHelper.get_page(self, "/portal/", "home/home_teacher.html")

    def test_portal_student(self):
        self.client.force_login(self.student)
        testHelper.get_page(self, "/portal/", "home/home_student.html")

    def test_portal_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get("/portal/", follow=True)
        self.assertRedirects(
            response, "/admin/login/?next=%2Fadmin%2F", status_code=302
        )

    def test_portal_caregiver(self):
        # Redirects to home page
        self.client.force_login(self.caregiver)
        response = self.client.get("/portal/", follow=True)
        self.assertRedirects(response, "/", status_code=302)

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


class TestErrorPages(TestCase):
    def test_403_page(self):
        # Create a view that will return a 403 error
        def view_403(request):
            raise PermissionError

        # create a request
        request = self.client.get("/").wsgi_request

        # Test that the view returns a 403 error
        with self.assertRaises(PermissionError):
            page403 = view_403(request)
            # Test that the 403 page is returned
            self.assertTemplateUsed(page403, "403.html")

    def test_404_page(self):
        # Create a view that will return a 404 error
        def view_404(request):
            raise FileNotFoundError

        # create a request
        request = self.client.get("/").wsgi_request

        # Test that the view returns a 404 error
        with self.assertRaises(FileNotFoundError):
            page404 = view_404(request)
            # Test that the 404 page is returned
            self.assertTemplateUsed(page404, "404.html")

    def test_500_page(self):
        # Create a view that will return a 500 error
        def view_500(request):
            raise Exception

        # create a request
        request = self.client.get("/").wsgi_request

        # Test that the view returns a 500 error
        with self.assertRaises(Exception):
            page500 = view_500(request)
            # Test that the 500 page is returned
            self.assertTemplateUsed(page500, "500.html")

    def test_missing_slash(self):
        # Test that a missing slash is redirected to the same URL with a trailing slash
        # Do this for a couple of random pages
        response = self.client.get("/contact")
        self.assertRedirects(response, "/contact/", status_code=301)
        response = self.client.get("/about")
        self.assertRedirects(response, "/about/", status_code=301)
        response = self.client.get("/privacy")
        self.assertRedirects(response, "/privacy/", status_code=301)
