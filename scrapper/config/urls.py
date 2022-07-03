from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from scrapper.config import settings
from scrapper.config.docs import SchemaView
from scrapper.core.views import ImageView, IndexView, ScrapeFormView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls, name="admin-view"),
    # Auth
    path(
        "logout/",
        LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
    # Auth API
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
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
    path("", IndexView.as_view(), name="index"),
    path("view/images", ScrapeFormView.as_view(), name="scrape-view"),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
