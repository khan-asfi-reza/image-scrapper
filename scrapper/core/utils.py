import re

from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as RestValidationError

# URL Regex
regex = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def check_if_valid_url(url: str):
    """
    Checks if a url is valid
    Args:
        url: str , The URL to check

    Returns: bool, If url is valid or not

    """
    return re.match(regex, url) is not None


def validate_url(url: str):
    """

    Django Model Validator

    Args:
        url: URL string

    Raises:
        Raises validation error if url is invalid

    """
    if not (check_if_valid_url(url)):
        raise ValidationError("Invalid URL")


def validate_url_drf(url: str):
    """
    Django Rest Framework Serializer Validator
    Args:
        url: URL String

    Raises:
        Raises validation error if url is invalid

    """
    if not (check_if_valid_url(url)):
        raise RestValidationError("Invalid URL")


def normalize_url(url: str) -> str:
    """
    Normalizes given url.
    Removes extra redundant slashes

    Args:
        url: URL String

    Returns:

    """
    segments = url.split("/")
    correct_segments = []
    for segment in segments:
        if segment != "":
            correct_segments.append(segment)
    first_segment = str(correct_segments[0])
    if first_segment.find("http") == -1:
        correct_segments = ["http:"] + correct_segments
    correct_segments[0] = correct_segments[0] + "/"
    normalized_url = "/".join(correct_segments)
    normalized_url = (normalized_url[:-1] if normalized_url[-1] == '/'
                      else normalized_url)
    return normalized_url
