from django.urls import path, re_path, include

from audiovisual.views import ImageCreateView

from herdi.views import (
    HerdView,
    contactlistview,
    invitationsendview,
    EventAutocomplete,
    EventTeacherAutocomplete,
    ImagesAutocomplete,
    IrregularityAutocomplete,
    PriceOptionAutocomplete,
    TeachersAutocomplete,
    TimeOptionAutocomplete,
    TimeLocationAutocomplete,
    UserAutocomplete,
    VideosAutocomplete,
)


urlpatterns = [
    path("", HerdView.as_view(), name="herd"),
    path("", include('project.urls')),
    path("", include('accounting.urls')),
    path("", include('booking.urls')),
    path("contact/", contactlistview, name="contact_list"),
    path("teacher/booking/invite/", invitationsendview, name="invitation"),
    path("image/create/", ImageCreateView.as_view(), name="image_create"),
    # Autocompletes
    re_path(r"^event-autocomplete/$", EventAutocomplete.as_view(), name="event-autocomplete"),
    re_path(r"^event-teacher-autocomplete/$", EventTeacherAutocomplete.as_view(), name="event-teacher-autocomplete"),
    re_path(r"^user-autocomplete/$", UserAutocomplete.as_view(), name="user-autocomplete"),
    re_path(r"^teachers-autocomplete/$", TeachersAutocomplete.as_view(), name="teachers-autocomplete"),
    re_path(r"^to-autocomplete/$", TimeOptionAutocomplete.as_view(), name="to-autocomplete"),
    re_path(r"^tl-autocomplete/$", TimeLocationAutocomplete.as_view(), name="tl-autocomplete"),
    re_path(r"^po-autocomplete/$", PriceOptionAutocomplete.as_view(), name="po-autocomplete"),
    re_path(r"^irregularities-autocomplete/$", IrregularityAutocomplete.as_view(), name="irregularities-autocomplete"),
    re_path(r"^images-autocomplete/$", ImagesAutocomplete.as_view(), name="images-autocomplete"),
    re_path(r"^videos-autocomplete/$", VideosAutocomplete.as_view(), name="videos-autocomplete"),
]
