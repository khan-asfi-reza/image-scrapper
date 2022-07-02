from django.urls import path

from scrapper.core.views import ImageView, URLViewSet, ImageDetailsView

urlpatterns = [
    path("url/", URLViewSet.as_view(), name="url-view"),
    path("image/details/<int:id>", ImageDetailsView.as_view(), name="image-detail-view"),
]
