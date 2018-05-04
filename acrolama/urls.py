from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from formulario.views import (
    fest_createview,
    festprueba_createview,
    )
from fest.views import (
    fest_homeview,
    fest_locationview,
    fest_pricesview,
    )

from home.views import (
    homeview,
    InfoDetailView,
    EventView,
    EventDetailView,
    PortfolioCreateView,
    )


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', LoginView.as_view(), name='login'),
    url(r'^$', homeview, name='home'),
    url(r'^portfolioupload/$', PortfolioCreateView.as_view()),
    url(r'^event/(?P<slug>[\w-]+)/$', EventView.as_view()),
    url(r'^info/(?P<slug>[\w-]+)/$', InfoDetailView.as_view()),
    url(r'^fest/$', fest_homeview),
    url(r'^fest/form/$', fest_createview),
    url(r'^fest/location/$', fest_locationview),
    url(r'^fest/prices/$', fest_pricesview),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
