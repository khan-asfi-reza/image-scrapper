from django.contrib import admin
from django.urls import include, path

from scrapper.config.docs import SchemaView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("scrapper.core.urls")),
    path(
        "api-docs/",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        SchemaView.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
