from django.test import TestCase
from commendationSite import testHelper

# Create your tests here.


class TestHomePages(TestCase):
    def test_home_page(self):
        testHelper.get_page(self, "/", "home/index.html")
