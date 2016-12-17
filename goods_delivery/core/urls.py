from django.conf.urls import url

from .views import MapView


urlpatterns = [
    url(r'map$', MapView.as_view(), name='map'),
]
