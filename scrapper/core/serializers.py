from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from scrapper.core.models import Address, Image
from scrapper.core.utils import validate_url


class URLBaseSerializer(serializers.Serializer):
    """
    Contains URL Fields, Base Serializer Returns Stored Images
    when save method is fired
    """
    url = serializers.URLField(validators=[validate_url], required=True)

    def update(self, instance, validated_data):
        """
        Abstract class method, does not require in this class
        Args:
            instance:
            validated_data:

        Returns:

        """
        raise NotImplemented

    def create(self, validated_data) -> QuerySet[Image]:
        """
        Returns Stored Image Objects from the database
        Args:
            validated_data: Dictionary

        Returns:

        """
        return Image.objects.filter(
            parent_url__url=validated_data.get("url")
        )


class URLCreateSerializer(URLBaseSerializer):
    """
    This serializer performs `Address.save_url_with_images`
    """

    def create(self, validated_data) -> QuerySet[Image]:
        """

        Performs `Address.save_url_with_images`

        Args:
            validated_data: Dictionary of validated data

        Returns:Image Queryset

        """
        try:
            images = Address.save_url_with_images(
                validated_data.get("url", None)
            )
        except DjangoValidationError:
            raise ValidationError({"url": "URL Does not exist"})
        return images


class URLDeleteAndRecreateSerializer(URLBaseSerializer):
    """
    This serializer deletes all available Image Instance
    and re-scrape and recreate Image Instances
    """

    def create(self, validated_data) -> QuerySet[Image]:
        """

        Performs `Address.restore_or_create`

        Args:
            validated_data: Dictionary of validated data

        Returns:Image Queryset

        """
        try:
            images = Address.restore_or_create(
                validated_data.get("url", None)
            )
        except DjangoValidationError:
            raise ValidationError({"url": "URL Does not exist"})
        return images


class ImageOriginalURLQuerySerializer(URLBaseSerializer):
    """
    Returns Queryset of Image Queried By Original Image URL
    """

    def create(self, validated_data):
        return Image.objects.filter(
            original_url=validated_data.get("url")
        )


class AddressSerializer(serializers.ModelSerializer):
    """

    Address Serializer

    Attributes:
        "id": Address ID
        "url": Address URL

    """

    class Meta:
        """
        Serializer Meta Class
        """

        model = Address
        fields = ["id", "url"]


class ImageSerializer(serializers.ModelSerializer):
    """
    Attributes:
        image_url: Sends the image viewing URL
        parent_url: Parent URL Refers to AddressSerializer to show nested data

    """

    image_url = serializers.HyperlinkedIdentityField(
        view_name="image-view", lookup_field="pk"
    )
    parent_url = AddressSerializer()

    class Meta:
        """
        Serializer Meta Class
        """

        model = Image
        fields = [
            "id",
            "image_url",
            "image_name",
            "parent_url",
            "original_url",
            "height",
            "width",
            "mode",
            "format",
            "created",
            "updated",
        ]
