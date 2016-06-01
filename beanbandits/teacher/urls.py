from django.conf.urls import url

from . import views

app_name = 'teacher'

urlpatterns = [
    url(r'^$', views.WordSetListView.as_view(), name='select'),
    url(r'^quiz/(?P<pk>[0-9]+)/$', views.quiz, name='quiz'),
    url(r'^index/$', views.index, name='index'),
]
