from urllib import response
from django.test import TestCase
import os, json

# Create your tests here.


class ApiTestCase(TestCase):
    def setUp(self):
        # Get the json data from the sampleCheck.json file
        with open(
            os.path.join(os.path.dirname(__file__), "sampleCheck.json")
        ) as json_file:
            json_data = json.load(json_file)

            correct_auth = f'Basic {os.getenv("KAMAR_AUTH_USERNAME")}/{os.getenv("KAMAR_AUTH_PASSWORD")}'

            self.good_req = self.client.post(
                "/api/check/",
                json_data,
                content_type="application/json",
                **{"HTTP_AUTHORIZATION": correct_auth},
            )
            self.bad_req = self.client.post(
                "/api/check/",
                json_data,
                content_type="application/json",
                **{"HTTP_AUTHORIZATION": "Basic invalid"},
            )

    def test_good_request(self):
        self.assertEqual(
            self.good_req.status_code,
            200,
            "Valid credentials were not accepted with 200",
        )

    def test_bad_request(self):
        self.assertEqual(
            self.bad_req.status_code,
            403,
            "Invalid credentials were not rejected with 403",
        )
