from typing import Optional

import requests
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, View

from scrapper.core.const import SUPPORTED_FORMATS
from scrapper.core.models import Address, Image


class ImageView(View):
    """
    Returns the Image using saved Image ID
    """

    model = Image
    # Query size Dictionary, refers to image width
    size = {"small": 256, "medium": 1024, "large": 2048}

    # Supported Image formats

    def get_image_size(self, key: str, request) -> Optional[int]:
        """
        If request query contains size return size else return None
        Args:
            key: Height or Width
            request: HTTP Request Dictionary

        Returns: int | None

        """
        req_size: str = request.GET.get(key, "")
        if req_size.isdigit():
            return int(req_size)
        return self.size.get(req_size, None)

    @staticmethod
    def get_quality(request) -> Optional[int]:
        """
        If request query contains quality return quality else return None
        Args:
            request: HTTP Request Dictionary

        Returns: int | None
        """
        req_size: str = request.GET.get("quality", "")
        if req_size.isdigit():
            return int(req_size)
        return 100

    def get(self, request, pk) -> HttpResponse:
        """
        Sends image to client using Image ID
        Optional Parameters:
            width: Width of the image
        Args:
            request: HTTP Request Dictionary
            pk: Image ID

        Returns:

        """
        image = get_object_or_404(self.model, pk=pk)
        width = self.get_image_size("width", request)
        height = self.get_image_size("height", request)
        quality = self.get_quality(request)
        img_format = request.GET.get("format", image.format)
        cropped_image = image.get_image_with_size(
            width=width,
            height=height,
        )
        content_type: str = (
            img_format
            if img_format in SUPPORTED_FORMATS
            else image.format_lower
        )

        response = HttpResponse(content_type=f"image/{content_type}")
        cropped_image.save(
            response, content_type.capitalize(), quality=quality
        )
        return response


class IndexView(View):
    """
    Home Page View
    """

    template_name = "index.html"

    def get(self, request):
        context = {
            "image_scrape_view": request.build_absolute_uri(
                reverse("scrape-view")
            )
        }
        return render(request, self.template_name, context)


class ScrapeFormView(View):
    @staticmethod
    def post(request, **kwargs):
        api_url = request.build_absolute_uri(reverse("url-view"))
        resp = requests.post(api_url, json={"url": request.POST.get("url")})
        if resp.status_code == 200:
            return render(
                request,
                template_name="image_list.html",
                context={"data": resp.json()},
            )
        return Http404("Invalid URL")
