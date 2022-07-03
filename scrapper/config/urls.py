from django.contrib import admin
from django.urls import include, path

from scrapper.config.docs import SchemaView
from scrapper.core.views import ImageView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Auth API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Core API
    path("api/", include("scrapper.core.urls")),
    path("image/<int:pk>", ImageView.as_view(), name="image-view"),
    # Docs
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
