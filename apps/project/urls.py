from django.urls import path

from project.views import (
    eventlistview,
    eventupdateview,
)

urlpatterns = [
    # Event
    path("events/", eventlistview, name="event_list"),
    path("event/<int:pk>/update/", eventupdateview, name="event_update"),
]
