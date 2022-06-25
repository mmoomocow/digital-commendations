from django.test import TestCase

# Create your tests here.


class testHomePage(TestCase):
    def test_home_page(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
