from django.urls import path

from booking.views import (
    attendancelistview,
    AttendanceUpdateView,
    bookinglistview,
    BookUpdateView,
    QuotationUpdateView,
    quotationlistview,
    quotationcreateview,
    quotationlockview,
)

urlpatterns = [
    # Booking
    path("book/", bookinglistview, name="booking_list"),
    path("book/<int:pk>/", BookUpdateView.as_view(), name="booking_update"),
    # Attendance
    path("attendance/", attendancelistview, name="attendance_list"),
    path("attendance/<int:pk>/", AttendanceUpdateView.as_view(), name="attendance_update"),
    # Quotation
    path("quotation/", quotationlistview, name="quotation_list"),
    path("quotation/<int:pk>/", QuotationUpdateView.as_view(), name="quotation_update"),
    path("quotation/<int:pk>/lock/", quotationlockview, name="quotation_lock"),
    path("quotation/create/", quotationcreateview, name="quotation_create"),
]
