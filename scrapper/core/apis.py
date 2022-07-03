from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from scrapper.core.models import Image
from scrapper.core.permissions import IsAdminOrStaff, CanDeleteOrGet
from scrapper.core.serializers import (
    URLCreateSerializer,
    ImageSerializer,
    URLDeleteAndRecreateSerializer,
    URLBaseSerializer, ImageOriginalURLQuerySerializer)


class URLImageScrappingAPI(GenericAPIView):
    """
    This view takes URL Parameter, scrapes images from the given URL
    and stores images along with meta data in the database
    """
    serializer_class = URLCreateSerializer

    @swagger_auto_schema(responses={200: ImageSerializer(many=True)}, )
    def post(self, request) -> Response:
        """

        Args:
            request: HttpRequest

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


class URLImagesDeleteScrapeAPI(URLImageScrappingAPI):
    """
    This view deletes all previous image records
    and recreate Image Instance after scraping
    Allow Only Admin Users and Staff Users
    """
    permission_classes = (IsAdminOrStaff,)
    serializer_class = URLDeleteAndRecreateSerializer


class ImageListAPI(URLImageScrappingAPI):
    """
    Returns saved List of through parent URL,
    It does not scrap the URL, it returns only the saved Data
    """
    serializer_class = URLBaseSerializer


class ImageDetailsAPI(RetrieveDestroyAPIView):
    """
    Returns Stored Image Details,
    including Image Preview Link,
    Original Link and MetaData
    """
    permission_classes = (CanDeleteOrGet,)
    lookup_field = "id"
    serializer_class = ImageSerializer
    queryset = Image.objects.get_queryset()


class ImageOriginalURLQueryAPI(APIView):
    """
    Performs query by `original_url` of the image,
    returns Image Data along with Metadata
    """
    serializer_class = ImageOriginalURLQuerySerializer

    @swagger_auto_schema(responses={200: ImageSerializer(many=True)}, )
    def post(self, request):
        """
        Args:
            request: HttpRequest

        Returns: Response

        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            image = ImageSerializer(instance=serializer.save())
            return Response(image.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
