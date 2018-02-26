"""acrolama URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from formulario.views import (
    fest_createview,
    festprueba_createview,
    cert
    )
from fest.views import (
    fest_homeview,
    fest_locationview,
    fest_pricesview,
    )
from home.views import (
    homeview,
    EventView,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', homeview),
    url(r'^event/$', EventView.as_view()),
    url(r'^fest/$', fest_homeview),
    url(r'^fest/form/$', fest_createview),
    url(r'^fest/location/$', fest_locationview),
    url(r'^fest/prices/$', fest_pricesview),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
