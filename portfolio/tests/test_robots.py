from http import HTTPStatus
from django.test import SimpleTestCase


class RobotsTxtTests(SimpleTestCase):
    def test_robots(self):
        response = self.client.get("/robots.txt")

        assert response.status_code == HTTPStatus.OK
        assert response["content-type"] == "text/plain"

    def test_sitemap(self):
        response = self.client.get("/sitemap.xml")

        assert response.status_code == HTTPStatus.OK
        assert response["content-type"] == "application/xml"
