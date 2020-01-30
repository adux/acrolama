from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from home.views import (
    HomeFormView,
    faqview,
    ClassListView,
    InfoDetailView,
    EventListView,
)
from project.views import EventDetail
from booking.views import (
    #Attendance
    attendance_daily_view,
    AttendanceMainListView,
    BookListView,
    BookUpdateView,
    BookCreateView,
    HerdView,
)

# Sitemap
from django.contrib.sitemaps.views import sitemap
from home.sitemaps import (
    StaticViewSitemap,
    InfoViewSite,
    EventViewSite,
    MainViewSitemap,
)

sitemaps = {
    'faq': StaticViewSitemap,
    'infos': InfoViewSite,
    'events': EventViewSite,
    'main' : MainViewSitemap,
}

urlpatterns = [
    # Users Registration
    path("accounts/", include("allauth.urls")),
    # Home
    path('', HomeFormView.as_view(), name="home"),
    path("events/", EventListView.as_view(), name="events"),
    path("classes/", ClassListView.as_view(), name="classes"),
    path("events/<slug:slug>/", EventDetail.as_view(), name="event"),
    path("classes/<slug:slug>/", EventDetail.as_view(), name="class"),
    path("info/<slug:slug>/", InfoDetailView.as_view(), name="info"),
    path("faq/", faqview, name="faq"),
    # Sitemaps
    path('sitemap.xml', sitemap,
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    # Admin stuff
    url(settings.ADMIN_URL, admin.site.urls),
    # TODO: Add to Admin url 
    path("herd/", HerdView.as_view(), name="herd"),
    path("herd/booking/", BookListView.as_view(), name="booking_list"),
    path("herd/booking/<int:pk>/update/", BookUpdateView.as_view(), name="booking_update"),
    path("herd/booking/create/", BookCreateView.as_view(), name="booking_create"),
    path("herd/accounting/", BookListView.as_view(), name="accounting_list"),
    path("herd/accounting/<int:pk>/update/", BookUpdateView.as_view(), name="accounting_update"),
    path("herd/accounting/create/", BookCreateView.as_view(), name="accounting_create"),
    path("herd/teacher/attendance", attendance_daily_view, name="teacher_attendance"),
    path("herd/attendance/", AttendanceMainListView.as_view(), name="attendance_list"),
    path("todo/", include("todo.urls", namespace="todo")),
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
