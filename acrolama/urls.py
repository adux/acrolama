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
from django.views.generic.base import TemplateView


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
    EventDetailView,
    FilePolicyAPI,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', homeview),
    url(r'^e/(?P<slug>[\w-]+)/$', EventDetailView.as_view()),
    url(r'^fest/$', fest_homeview),
    url(r'^fest/form/$', fest_createview),
    url(r'^fest/location/$', fest_locationview),
    url(r'^fest/prices/$', fest_pricesview),
    url(r'^api/files/policy/$', FilePolicyAPI.as_view()),
    url(r'^upload/$', TemplateView.as_view(template_name='upload.html'), name='upload-home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
''' 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
