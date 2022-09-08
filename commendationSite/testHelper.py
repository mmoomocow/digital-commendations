# Test Helper, contains functions to help with testing

from django.test import TestCase

# Basic page tester, takes a path and template name
def testPage(self: TestCase, path: str, template: str):
    page = self.client.get(path)
    self.assertEqual(
        page.status_code, 200, f"Page {path} returned {page.status_code} instead of 200"
    )
    self.assertTemplateUsed(page, "base.html", f"Page {path} did not use base.html")
    self.assertTemplateUsed(page, template, f"Page {path} did not use {template}")
