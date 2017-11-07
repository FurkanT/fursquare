from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^venues/$', views.venue_list),
    url(r'^comments/$', views.comment_list),
    url(r'^venues/(?P<pk>[0-9]+)/$', views.venue_detail),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.comment_detail),
]
