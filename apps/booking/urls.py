from django.urls import path

from booking.views import (
    attendance_daily_view,
    attendancelistview,
    AttendanceUpdateView,
    bookinglistview,
    BookUpdateView,
    BookCreateView,
    QuotationUpdateView,
    quotationlistview,
    quotationcreateview,
    quotationlockview,
)

urlpatterns = [
    # Booking
    path("", bookinglistview, name="booking_list"),
    path("<int:pk>/", BookUpdateView.as_view(), name="booking_update"),
    # Attendance
    path("attendance/", attendancelistview, name="attendance_list"),
    path("attendance/<int:pk>/", AttendanceUpdateView.as_view(), name="attendance_update"),
    # Quotation
    path("quotation/", quotationlistview, name="quotation_list"),
    path("quotation/<int:pk>/", QuotationUpdateView.as_view(), name="quotation_update"),
    path("quotation/<int:pk>/lock/", quotationlockview, name="quotation_lock"),
    path("quotation/create/", quotationcreateview, name="quotation_create"),
]
