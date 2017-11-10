from django.conf.urls import url
from django.conf.urls import include
from rest_framework.authtoken import views as token_views
from . import views

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^venues/$', views.venue_list),
    url(r'^comments/$', views.comment_list),
    url(r'^ratings/$', views.rating_list),
    url(r'^venue-types/$', views.venue_type_list),
    url(r'^user-list/$', views.user_list),
    url(r'^venues/(?P<pk>[0-9]+)/$', views.venue_detail),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.comment_detail),
    url(r'^venue-types/(?P<pk>[0-9]+)$', views.venue_type_detail),
    url(r'^rating-details/(?P<pk>[0-9]+)$', views.rating_detail),
    url(r'^user-details/(?P<pk>[0-9]+)$', views.user_detail),
    url(r'^venues/(?P<pk>[0-9]+)/ratings$', views.venue_rating_list),
    url(r'^venues/(?P<venue_pk>[0-9]+)/ratings/(?P<rating_pk>[0-9]+)/$', views.venue_rating_detail),
    url(r'^api-token-auth/', token_views.obtain_auth_token)
]
