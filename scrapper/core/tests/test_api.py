import shutil
import tempfile
from io import BytesIO

from django.test import Client
from django.urls import reverse
from PIL import Image as PILImage
from rest_framework.test import APITestCase, override_settings

from scrapper.core.models import Image

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestAPI(APITestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_url_api(self):
        """
        Test API To Return Status Code 200
        """
        test_url = "https://picsum.photos/"
        url = reverse("url-view")
        resp = self.client.post(url, {"url": test_url})
        self.assertEqual(resp.status_code, 200)

    def test_url_api_fail(self):
        """
        Test API to fail and return status code 400
        """
        test_url = "http://abcdefg.test.test/xyz/"
        url = reverse("url-view")
        resp = self.client.post(url, {"url": test_url})
        self.assertEqual(resp.status_code, 400)

    def get_image_and_url(self):
        self.test_url_api()
        image = Image.objects.latest("id")
        url = reverse("image-view", kwargs={"pk": image.id})
        return image, url

    def test_image_api_with_size(self):
        """
        Test Image Content
        """
        image, url = self.get_image_and_url()
        client = Client()
        resp = client.get(url)
        img = PILImage.open(BytesIO(resp.content))
        self.assertAlmostEqual(img.height, image.height)
        self.assertAlmostEqual(img.width, image.width)
