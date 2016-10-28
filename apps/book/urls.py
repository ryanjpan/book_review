from django.conf.urls import url, include
from . import views
from django.core.urlresolvers import reverse

urlpatterns = [
    url(r'^$', views.book, name='book'),
    url(r'^addreview$', views.addreview, name='addreview'),
    url(r'^insertreview$', views.insertreview, name='insertreview'),
    url(r'^book/(?P<id>\d+)$', views.title, name='title'),
]
