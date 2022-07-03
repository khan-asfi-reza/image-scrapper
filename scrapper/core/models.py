import math
from io import BytesIO
from typing import Any, List, Optional
from urllib.parse import urlparse

import PIL
import requests
import urllib3
from PIL import Image as PilImage
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from scrapper.core.utils import check_if_valid_url, normalize_url, validate_url


class AbstractModel(models.Model):
    """

    Abstract model containing `created` and `updated` model field
    The model which will inherit AbstractModel will have the above
    2 fields by default

    Attributes:
        `created`: Timestamp the data creation time
        `updated`: Timestamp the data update time

    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """

        Meta class that contains meta data for this model
        Attributes:
            abstract = True; as this is an abstract model

        """

        abstract = True


class Address(AbstractModel):
    """

    Stores Queried model, inherits AbstractModel
    to have `created` and `updated` field by default

    Attributes:
        `name`: The queried URL

    """

    url = models.URLField(
        unique=True,
        db_index=True,
        validators=[
            validate_url,
        ],
    )
    http_response = None

    @property
    def netloc(self) -> str:
        """

        Returns: str, Domain address of the url / Net location of the url instance

        """
        return urlparse(self.url).netloc

    def __str__(self) -> str:
        """
        Model string format

        Returns: Model String

        """
        return self.url

    @classmethod
    def save_url_with_images(cls, url: str) -> QuerySet:
        """
        Given a URL, it saves the URL as Address Object
        and scrapes the url to store the images
        Args:
            url: URL to scrap the images from

        Returns: QuerySet<Image>, scrapped and saved images

        """
        # Checks if a url already exists in the database which has been scrapped
        # Otherwise create the url record
        url_object, created = cls.objects.get_or_create(url=url)
        # Image Saving Procedure
        return Image.save_multiple_images(url_object)

    @classmethod
    def sync_url_images(cls):
        """
        Future Celery Background Task
        It will sync images, check if there are new images
        in the url, save them
        """
        addresses = cls.objects.all()
        for address in addresses:
            cls.save_url_with_images(address.url)

    @classmethod
    def restore_or_create(cls, url) -> QuerySet:
        """
        Given a URL, it saves the URL as Address Object
        and Deletes previous Images and Restore them
        Args:
            url: URL to scrap the images from

        Returns: QuerySet<Image>, scrapped and saved images
        """
        # Checks if a url already exists in the database which has been scrapped
        # Otherwise create the url record
        url_object, created = cls.objects.get_or_create(url=url)
        # Utility function that scrapes data from a html file
        return Image.remove_all_and_restore(url_object)


@receiver(post_save, sender=Address)
def normalize_url_before_save(
        sender: Address, instance: Address, *args, **kwargs
):
    """
    Normalizes url before saving it, removes unnecessary slashes
    Args:
        sender: Address Model
        instance: Address Model Instance
        *args:
        **kwargs:

    Returns:

    """
    instance.url = normalize_url(instance.url)


def image_directory(instance, filename) -> str:
    """
    Gets image directory name
    Args:
        filename: Name of the image file
        instance: Image Model Instance

    Returns: directory name

    """
    return f"{instance.parent_url.netloc}/{instance.image_name}"


class Image(AbstractModel):
    """

    Scrapped Images, inherits AbstractModel
    to have `created` and `updated` field by default

    Attributes:
        `url`: Parent URL, Refers to Address Model
        `image`: Image instance scrapped from the url
        `image_name`: Image filename
        `height`: Image Height in px
        `width`: Image width in px
        `mode`: Image mode Metadata, Example: 'RGB', 'CMYK'
        `format`: Image file format, Example: 'JPEG', 'GIF'

    """

    parent_url = models.ForeignKey(
        to=Address, on_delete=models.SET_NULL, null=True
    )
    original_url = models.URLField(blank=True)
    image = models.ImageField(upload_to=image_directory, null=True, blank=True)
    image_name = models.CharField(max_length=500)
    height = models.FloatField()
    width = models.FloatField()
    mode = models.CharField(max_length=100)
    format = models.CharField(max_length=100)

    @property
    def format_lower(self) -> str:
        """

        Returns: Image format in lower case

        """
        return self.format.lower()

    def __str__(self) -> str:
        """

        Returns: Model String Representation

        """
        return f"{self.image_name}"

    def get_image_with_size(
            self,
            width: Optional[float] = None,
            height: Optional[float] = None,
    ) -> Any:
        """
        Returns image with custom width or height
        If given both height or width then only width will work,
        maintaining ratio

        Args:
            height: Height of the image
            width: Width of the image

        Returns:

        """
        pil_image = PilImage.open(self.image)
        size = (self.width, self.height)
        if width and width < self.width:
            _height = (width / self.width) * self.height
            size = tuple(map(math.floor, [width, _height]))

        elif height and height < self.height:
            _width = (height / self.height) * self.width
            size = tuple(map(math.floor, [_width, height]))

        pil_image.thumbnail(size)

        return pil_image

    @staticmethod
    def get_images_from_url_response(url: str) -> List[str]:
        """
        Given a URL, this method scraps through the document
        using BS4 Module. Finds all <img/> tag and gets the source from it
        then returns the list of image source found from <img/> tag located in
        the document
        Args:
            url: str

        Returns: List[str], Returns List of image url

        """
        try:
            resp = requests.get(url).text
        except requests.exceptions.ConnectionError:
            raise ValidationError("Invalid URL")
        # Parse HTML
        soup = BeautifulSoup(resp, "html.parser")
        # Find images from the HTML Doc
        images = soup.find_all("img")
        # Get Image source/url
        img_list = [img["src"] for img in images]
        return img_list

    @classmethod
    def save_image(cls, image_url: str, url: Address):
        """
        Saves Images from a given URL along with Metadata
        Args:
            image_url: Image Link
            url: Parent Url Address

        Returns:

        """
        if image_url.startswith("/"):
            image_url = image_url[1:]
        img_url = (
            image_url
            if check_if_valid_url(image_url)
            else f"{url.url}/{image_url}"
        )
        try:
            response = requests.get(img_url)
            pillow_image = PilImage.open(BytesIO(response.content))
            file_bytes = BytesIO()
            file_name = (
                f"{get_random_string(length=32)}."
                f"{pillow_image.get_format_mimetype().split('/')[-1]}"
            )
            img_object = cls.objects.create(
                parent_url=url,
                image_name=file_name,
                original_url=img_url,
                height=pillow_image.height,
                width=pillow_image.width,
                mode=pillow_image.mode,
                format=pillow_image.format,
            )
            pillow_image.save(file_bytes, pillow_image.format)
            img_object.image.save(
                file_name,
                File(file_bytes),
            )
            img_object.save()
        except (
                PIL.UnidentifiedImageError,
                urllib3.exceptions.LocationParseError,
        ):
            pass

    @classmethod
    def __save_multi_from_url(cls, images: List[str], url: Address):
        for image in images:
            cls.save_image(image, url)

    @classmethod
    def get_queryset_by_url(cls, parent_url: Address):
        return cls.objects.filter(parent_url=parent_url)

    @classmethod
    def save_multiple_images(cls, url: Address) -> QuerySet:
        """
        Given URL Address, it saves all images scrapped from the url in the database and media
        directory,
        Steps:
            1. Scrape image from the URL and get list of those images
               by calling `get_images_from_url_response`

            2. Find cached image of the URL, if the api runs for the first time for a URL 'X'
               the link of the images scrapped from 'X' will be cached.

            3. Compare cached links and scraped links, if they are the same,
               return filtered queryset

            4. Loops through all images create image model instance
        Args:
            url: Address Instance

        Returns: QuerySet<Image> Returns all images scrapped from the url

        """
        # Scraps image through the given URL
        images = cls.get_images_from_url_response(url.url)
        # Get cached Image Link
        cached_image = cache.get(url.url, [])
        # Remove common links
        all_images = list(set(images) - set(cached_image))  # Removes Duplicates
        # Set new cache
        cache.set(url.url, list(all_images) + list(cached_image), None)
        # Save Multiple Images
        cls.__save_multi_from_url(all_images, url=url)
        # Return Queryset
        return cls.get_queryset_by_url(parent_url=url)

    @classmethod
    def remove_all_and_restore(cls, url: Address) -> QuerySet:
        """
        Removes all available images and re-scrape images
        Removes from file storage as well
        Args:
            url: URL String

        Returns:

        """
        # Delete all available images
        cls.objects.all().delete()
        # Restore images
        images = list(set(cls.get_images_from_url_response(url.url)))  # Remove duplicates
        cls.__save_multi_from_url(images, url=url)
        # Set Cache
        cache.set(url.url, images, None)
        # Return Queryset
        return cls.get_queryset_by_url(parent_url=url)


@receiver(post_delete, sender=Image)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except FileNotFoundError:
        pass
