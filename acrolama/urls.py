from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from home.views import (
    HomeFormView,
    faqview,
    accountingview,
    ClassListView,
    InfoDetailView,
    EventListView,
    )
from project.views import EventDetail

urlpatterns = [
    #Users Registration
    path('accounts/', include('allauth.urls')),
    #Home
    url(r'^$', HomeFormView.as_view(), name='home'),
    url(r'^events/$', EventListView.as_view(), name='events'),
    url(r'^classes/$', ClassListView.as_view(), name='classes'),
    path('events/<slug:slug>/', EventDetail.as_view(), name='event'),
    path('classes/<slug:slug>/', EventDetail.as_view(), name='class'),
    url(r'^info/(?P<slug>[\w-]+)/$', InfoDetailView.as_view(), name='info'),
    path('faq/',faqview),
    #Admin stuff
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'^accounting/$', accountingview , name='accounting'),
    path('todo/', include('todo.urls', namespace="todo")),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
