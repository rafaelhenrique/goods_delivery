from django.conf.urls import url

from .views import MapDetailShortPathView, MapDetailView, MapView

urlpatterns = [
    url(r'map$', MapView.as_view(), name='map'),
    url(r'map/(?P<map_id>[a-z0-9_-]+)$', MapDetailView.as_view(),
        name='map_detail'),
    url(r'map/(?P<map_id>[a-z0-9_-]+)/shortpath$',
        MapDetailShortPathView.as_view(),
        name='map_detail_short_path'),
]
