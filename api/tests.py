from django.test import TestCase
from base64 import b64encode
import os, json

# Create your tests here.


def basicAuth(username, password):
    return "Basic {}".format(
        b64encode(
            "{}:{}".format(
                username,
                password,
            ).encode("utf-8")
        ).decode("utf-8")
    )


class ApiTestCase(TestCase):
    def setUp(self):
        # Get the json data from the sampleCheck.json file
        with open(
            os.path.join(os.path.dirname(__file__), "sampleCheck.json")
        ) as json_file:
            self.json_data = json.load(json_file)

    def test_good_request(self):
        # Send a request with the correct credentials
        good_req = self.client.post(
            "/api/check/",
            self.json_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=basicAuth(
                os.environ.get("KAMAR_AUTH_USERNAME"),
                os.environ.get("KAMAR_AUTH_PASSWORD"),
            ),
        )

        self.assertEqual(
            good_req.status_code,
            200,
            "Valid credentials were not accepted with 200",
        )

    def test_bad_request(self):
        # Send a request with the incorrect credentials
        bad_req = self.client.post(
            "/api/check/",
            self.json_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=basicAuth(
                "bad_username",
                "bad_password",
            ),
        )

        self.assertEqual(
            bad_req.status_code,
            403,
            "Invalid credentials were not rejected with 403",
        )

    def test_no_auth(self):
        # Send a request with no credentials
        no_auth_req = self.client.post(
            "/api/check/",
            self.json_data,
            content_type="application/json",
        )

        self.assertEqual(
            no_auth_req.status_code,
            403,
            "No credentials were not rejected with 403",
        )
