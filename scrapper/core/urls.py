from django.urls import path

from scrapper.core.apis import (
    ImageDetailsAPI,
    ImageListAPI,
    ImageOriginalURLQueryAPI,
    URLImageScrappingAPI,
    URLImagesDeleteScrapeAPI,
)

urlpatterns = [
    path("url/", URLImageScrappingAPI.as_view(), name="url-view"),
    path("images/list/", ImageListAPI.as_view(), name="image-list-view"),
    path(
        "images/restore/",
        URLImagesDeleteScrapeAPI.as_view(),
        name="image-restore-view",
    ),
    path(
        "images/details/<int:id>",
        ImageDetailsAPI.as_view(),
        name="image-detail-view",
    ),
    path(
        "images/query/",
        ImageOriginalURLQueryAPI.as_view(),
        name="image-query-view",
    ),
]
