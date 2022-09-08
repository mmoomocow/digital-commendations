from django.test import TestCase
from commendationSite import testHelper

# Create your tests here.


class TestHomePages(TestCase):
    def test_home_page(self):
        testHelper.testPage(self, "/", "home/index.html")
