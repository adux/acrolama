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
    # Attendance
    path("attendances/", attendancelistview, name="attendance_list"),
    path("attendance/<int:pk>/update/", AttendanceUpdateView.as_view(), name="attendance_update"),
    # Booking
    path("bookings/", bookinglistview, name="booking_list"),
    path("booking/<int:pk>/update/", BookUpdateView.as_view(), name="booking_update"),
    # Quotation
    path("quotations/", quotationlistview, name="quotation_list"),
    path("quotation/<int:pk>/update/", QuotationUpdateView.as_view(), name="quotation_update"),
    path("quotation/<int:pk>/lock/", quotationlockview, name="quotation_lock"),
    path("quotation/create/", quotationcreateview, name="quotation_create"),
    # Teacher
    path("teacher/attendance/", attendance_daily_view, name="teacher_attendance"),
    path("teacher/booking/create/", BookCreateView.as_view(), name="teacher_booking_create"),
]
