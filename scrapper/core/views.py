from typing import Optional

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from scrapper.core.models import Image
from scrapper.core.serializers import ImageSerializer, URLCreateSerializer


class URLViewSet(GenericAPIView):
    """
    URL ViewSet
    Examples:
        api: '/url'
        method: POST
        data: {url: str}

    This view takes URL Parameter and returns list of images, those are in the URL document

    """

    serializer_class = URLCreateSerializer

    @swagger_auto_schema(responses={200: ImageSerializer(many=True)})
    def post(self, request) -> Response:
        """
        Takes URL, and returns List of images scrapped from the URL

        Args:
            request: HTTP Request Dictionary

        Returns: Response

        """
        url = self.serializer_class(data=request.data)
        if url.is_valid():
            queryset = url.save()
            serializer = ImageSerializer(
                instance=queryset, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(url.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageView(View):
    """
    Returns the Image using saved Image ID
    """

    model = Image
    # Query size Dictionary, refers to image width
    size = {"small": 256, "medium": 1024, "large": 2048}

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
        cropped_image = image.get_image_with_size(width=width, height=height)
        response = HttpResponse(content_type=f"image/{image.format_lower}")
        cropped_image.save(response, image.format)
        return response