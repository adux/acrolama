from django.db import models


# Events
class EventRelatedManager(models.Manager):
    def get_queryset(self):
        return (
            super(EventRelatedManager, self)
            .get_queryset()
            .select_related("project", "policy", "discipline", "level")
            .prefetch_related(
                "time_locations",
                "irregularities",
                "price_options",
                "images",
                "videos",
                "teachers",
                "team",
            )
        )
