from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from project.models import Event
from home.models import Info


class StaticViewSitemap(Sitemap):
    priority = 0.4
    changefreq = "monthly"

    def items(self):
        return ["faq"]

    def location(self, item):
        return reverse(item)


class InfoViewSite(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return Info.objects.all()


class EventViewSite(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Event.objects.filter(published=True)


class MainViewSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return ["home", "events", "classes"]

    def location(self, item):
        return reverse(item)
