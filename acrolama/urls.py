from django.urls import path, include, re_path
from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin
# TODO: Cache
from django.views.decorators.cache import cache_page

from home.views import (
    HomeFormView,
    faqview,
    ClassListView,
    InfoDetailView,
    EventListView,
)

from project.views import (
    EventUpdateView,
    EventDetail,
    eventlistview,
)

from booking.views import (
    EventAutocomplete,
    EventTeacherAutocomplete,
    UserAutocomplete,
    attendance_daily_view,
    attendancelistview,
    AttendanceUpdateView,
    bookinglistview,
    BookUpdateView,
    BookCreateView,
    contactlistview,
    HerdView,
    invitationsendview,
    IrregularityAutocomplete,
    QuotationUpdateView,
    quotationlistview,
    quotationcreateview,
    quotationlockview,
    TimeLocationAutocomplete,
    TeachersAutocomplete,
    PriceOptionAutocomplete,
    TimeOptionAutocomplete,
)

from accounting.views import (
    accountinglistview,
    InvoiceUpdateView,
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
    "faq": StaticViewSitemap,
    "infos": InfoViewSite,
    "events": EventViewSite,
    "main": MainViewSitemap,
}

urlpatterns = [
    # Users Registration
    path("accounts/", include("allauth.urls")),
    # Home
    path("", HomeFormView.as_view(), name="home"),
    path("events/", EventListView.as_view(), name="events"),
    path("classes/", ClassListView.as_view(), name="classes"),
    # path("events/<slug:slug>/", cache_page(60*60)(EventDetail.as_view()), name="event"),
    path("events/<slug:slug>/", EventDetail.as_view(), name="event"),
    path("classes/<slug:slug>/", EventDetail.as_view(), name="class"),
    path("info/<slug:slug>/", InfoDetailView.as_view(), name="info"),
    path("faq/", faqview, name="faq"),
    # Sitemaps
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    # Profile
    # Admin stuff
    path(settings.ADMIN_URL, admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path("herd/", HerdView.as_view(), name="herd"),
    # Accounting
    path("herd/invoices/", accountinglistview, name="accounting_list"),
    path("herd/invoice/<int:pk>/update/", InvoiceUpdateView.as_view(), name="accounting_update"),
    # Attendance
    path("herd/attendance/", attendancelistview, name="attendance_list"),
    path("herd/attendance/<int:pk>/update/", AttendanceUpdateView.as_view(), name="attendance_update"),
    # Booking
    path("herd/booking/", bookinglistview, name="booking_list"),
    path("herd/booking/<int:pk>/update/", BookUpdateView.as_view(), name="booking_update"),
    # Event
    path("herd/event/", eventlistview, name="event_list"),
    path("herd/event/<int:pk>/update/", cache_page(60*60)(EventUpdateView), name="event_update"),
    # Quotation
    path("herd/quotation/", quotationlistview, name="quotation_list"),
    path("herd/quotation/<int:pk>/update/", QuotationUpdateView.as_view(), name="quotation_update"),
    path("herd/quotation/<int:pk>/lock/", quotationlockview, name="quotation_lock"),
    path("herd/quotation/create/", quotationcreateview, name="quotation_create"),
    # Contact
    path("herd/contact/", contactlistview, name="contact_list"),
    # Teachers
    path("herd/teacher/attendance/", attendance_daily_view, name="teacher_attendance"),
    path("herd/teacher/booking/create/", BookCreateView.as_view(), name="teacher_booking_create"),
    path("herd/teacher/booking/invite/", invitationsendview, name="invitation"),
    path("invitations/", include('invitations.urls', namespace="invitations")),
    re_path(r"^event-autocomplete/$", EventAutocomplete.as_view(), name="event-autocomplete"),
    re_path(r"^event-teacher-autocomplete/$", EventTeacherAutocomplete.as_view(), name="event-teacher-autocomplete"),
    re_path(r"^user-autocomplete/$", UserAutocomplete.as_view(), name="user-autocomplete"),
    re_path(r"^teachers-autocomplete/$", TeachersAutocomplete.as_view(), name="teachers-autocomplete"),
    re_path(r"^to-autocomplete/$", TimeOptionAutocomplete.as_view(), name="to-autocomplete"),
    re_path(r"^tl-autocomplete/$", TimeLocationAutocomplete.as_view(), name="tl-autocomplete"),
    re_path(r"^po-autocomplete/$", PriceOptionAutocomplete.as_view(), name="po-autocomplete"),
    re_path(r"^irregularities-autocomplete/$", IrregularityAutocomplete.as_view(), name="irregularities-autocomplete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
