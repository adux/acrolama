from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from django.urls import path, include

from home.views import (
    ClassListView,
    EventListView,
    faqview,
    HomeFormView,
    InfoDetailView,
    ProfileView,
)

from project.views import EventDetail

# Sitemap
from home.sitemaps import (
    StaticViewSitemap,
    InfoViewSite,
    EventViewSite,
    MainViewSitemap,
)

sitemaps = {
    "faq": StaticViewSitemap,
    "infos": InfoViewSite,
    "events": EventViewSite,
    "main": MainViewSitemap,
}

urlpatterns = [
    # Base_Home
    path("", HomeFormView.as_view(), name="home"),
    path("h/", ProfileView.as_view(), name="profile"),
    path("accounts/", include("allauth.urls")),
    path("events/", EventListView.as_view(), name="events"),
    path("events/<slug:slug>/", EventDetail.as_view(), name="event"),
    path("classes/", ClassListView.as_view(), name="classes"),
    path("classes/<slug:slug>/", EventDetail.as_view(), name="class"),
    path("info/<slug:slug>/", InfoDetailView.as_view(), name="info"),
    path("faq/", faqview, name="faq"),
    # Base_Admin
    path(settings.ADMIN_URL, admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    # Base_BootStrap
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("herd/", include("herdi.urls")),
    # Sitemaps
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns
