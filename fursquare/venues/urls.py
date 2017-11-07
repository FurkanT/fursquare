from django.conf.urls import url
from django.conf.urls import include

from . import views

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^venues/$', views.venue_list),
    url(r'^comments/$', views.comment_list),
    url(r'^venues/(?P<pk>[0-9]+)/$', views.venue_detail),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.comment_detail),
]
