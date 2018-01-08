"""cfehome URL Configuration

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
from django.views.generic import TemplateView
from clases.views import HomeView
from formulario.views import (
        fest_createview,
        festprueba_createview,
        cert
    )
from fest.views import (
        fest_homeview,
    )


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', fest_createview),
#    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
#    url(r'^contact/$', TemplateView.as_view(template_name='contact.html')),
    url(r'^fest/$', fest_createview),
    url(r'^festprueba/$', fest_homeview),
    url(r'^\.well-known/', include('letsencrypt.urls'))
]

#if not settings.DEBUG:
#    urlpatterns += patterns('',
#        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#    )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


