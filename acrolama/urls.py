from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from home.views import (
    homeview,
    faqview,
    accountingview,
    ClassListView,
    InfoDetailView,
    EventListView,
    )
from project.views import EventDetail
from users import views as user_views

urlpatterns = [
    #Users Registration
    path('register/', user_views.register, name='register'),
    #Home
    url(r'^$', homeview, name='home'),
    url(r'^events/$', EventListView.as_view(), name='events'),
    url(r'^classes/$', ClassListView.as_view(), name='classes'),
    path('events/<slug:slug>/', EventDetail.as_view(), name='event'),
    path('classes/<slug:slug>/', EventDetail.as_view(), name='class'),
    url(r'^info/(?P<slug>[\w-]+)/$', InfoDetailView.as_view(), name='info'),
    path('faq/',faqview),
    #Admin stuff
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'^accounts/login/', LoginView.as_view(), name='login'),
    url(r'^accounting/$', accountingview , name='accounting'),
    path('todo/', include('todo.urls', namespace="todo")),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
