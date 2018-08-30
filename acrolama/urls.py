from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from home.views import (
    homeview,
    accountingview,
    ClassListView,
    ClassDetailView,
    InfoDetailView,
    EventDetailView,
    EventListView,
    PortfolioCreateView,
    )

urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'^accounts/login/', LoginView.as_view(), name='login'),
    url(r'^accounting/$', accountingview , name='accounting'),
    url(r'^$', homeview, name='home'),
    url(r'^portfolioupload/$', PortfolioCreateView.as_view()),
    url(r'^events/$', EventListView.as_view(), name='event'),
    url(r'^classes/$', ClassListView.as_view(), name='class'),
    url(r'^events/(?P<slug>[\w-]+)$', EventDetailView.as_view(), name='events'),
    url(r'^classes/(?P<slug>[\w-]+)$', ClassDetailView.as_view(), name='classes'),
    url(r'^info/(?P<slug>[\w-]+)/$', InfoDetailView.as_view(), name='info'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
