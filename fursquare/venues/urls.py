from django.conf.urls import url
from django.conf.urls import include
from rest_framework.authtoken import views as token_views
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name="main_page"),
    url(r'^venues/(?P<pk>[0-9]+)/$', views.venue_detail_page, name="venue-detail"),
    url(r'^venue-types/(?P<slug>[\w-]+)/$', views.venue_page, name="venues"),
    url(r'^venue-types/(?P<slug>[\w-]+)/(?P<pk>[0-9]+)/$', views.check_and_direct_to_venue_detail_page,
        name="direct-to-venue-detail"),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api/venues/$', views.venue_list),
    url(r'^api/comments/$', views.comment_list),
    url(r'^api/ratings/$', views.rating_list),
    url(r'^api/venue-types/$', views.venue_type_list),
    url(r'^api/user-list/$', views.user_list),
    url(r'^api/venues/(?P<pk>[0-9]+)/$', views.venue_detail),
    url(r'^api/comments/(?P<pk>[0-9]+)/$', views.comment_detail),
    url(r'^api/venue-types/(?P<pk>[0-9]+)/$', views.venue_type_detail),
    url(r'^api/rating-details/(?P<pk>[0-9]+)/$', views.rating_detail),
    url(r'^api/user-details/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^api/venues/(?P<pk>[0-9]+)/ratings/$', views.venue_rating_list),
    url(r'^api/venues/(?P<venue_pk>[0-9]+)/ratings/(?P<rating_pk>[0-9]+)/$', views.venue_rating_detail),
    url(r'^api/token-auth/', token_views.obtain_auth_token),
    url(r'^api/login/$', views.login),



]
