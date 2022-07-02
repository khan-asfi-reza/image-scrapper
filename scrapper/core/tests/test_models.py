import shutil
import tempfile
from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from scrapper.core.models import Address, Image

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestCoreModels(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_address_model(self):
        """
        Tests if model is creating without error
        """
        test_url = "https://www.example.com/test/case"
        address = Address.objects.create(url=test_url)
        parsed_url = urlparse(test_url)
        self.assertEqual(parsed_url.netloc, address.netloc)

    def test_address_fail(self):
        """
        Test if Model is giving invalid URL Error
        """
        test_url = "sttps://a.b.c"
        try:
            Address.objects.create(url=test_url)
        except ValidationError as e:
            self.assertIn("Invalid URL", e.message)

    def test_address_pre_save(self):
        """
        Test if URL is normalized
        """
        test_url = "https://www.example.com///test///case"
        address = Address.objects.create(url=test_url)
        self.assertNotEqual(address.url, test_url)

    def test_address_with_url(self):
        """
        Test web scrapping model save method
        """
        test_url = "https://picsum.photos/"
        Image.save_multiple_images(Address.objects.create(url=test_url))
