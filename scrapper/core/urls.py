from django.urls import path

from scrapper.core.views import ImageView, URLViewSet

urlpatterns = [
    path("url/", URLViewSet.as_view(), name="url-view"),
    path("image/<int:pk>", ImageView.as_view(), name="image-view"),
]
