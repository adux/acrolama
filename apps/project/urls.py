from django.urls import path

from project.views import (
    eventlistview,
    eventupdateview,
)

urlpatterns = [
    # Event
    path("", eventlistview, name="event_list"),
    path("<int:pk>/", eventupdateview, name="event_update"),
]
