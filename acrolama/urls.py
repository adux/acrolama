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
    ControlListView,
    ControlUpdateView,
    ControlCreateView,
    HerdView,
)

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
    # Admin stuff
    url(settings.ADMIN_URL, admin.site.urls),
    path("herd/", HerdView.as_view(), name="herd"),
    path("herd/control/", ControlListView.as_view(), name="control_list"),
    path("herd/control/<int:pk>/update/", ControlUpdateView.as_view(), name="control_update"),
    path("herd/control/create/", ControlCreateView.as_view(), name="control_create"),
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
