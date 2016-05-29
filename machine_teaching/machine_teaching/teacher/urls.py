from django.conf.urls import patterns, include, url
from django.contrib import admin

from teacher import views

admin.autodiscover()

urlpatterns = patterns('',
url(r'^$', views.index, name='index'),
url(r'^admin/', include(admin.site.urls)),
)