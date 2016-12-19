import json
from uuid import uuid4
from decimal import Decimal

import pytest
from django.core.urlresolvers import reverse
from mixer.backend.django import mixer
from rest_framework import status

from goods_delivery.core.models import Map, Route


@pytest.mark.django_db
class TestMapView:

    @pytest.fixture
    def correct_payload(self):
        payload = {
            'name': 'Map01',
            'routes': [
                {'start': 'A', 'end': 'B', 'distance': 10},
                {'start': 'B', 'end': 'D', 'distance': 15},
                {'start': 'A', 'end': 'C', 'distance': 20},
                {'start': 'C', 'end': 'D', 'distance': 30},
                {'start': 'B', 'end': 'E', 'distance': 50},
                {'start': 'D', 'end': 'E', 'distance': 30},
            ],
        }
        return json.dumps(payload)

    @pytest.fixture
    def missing_fields_payload(self):
        payload = {
            'name': 'Map01',
            'routes': [
                {'start': 'A', 'distance': 10},
                {'start': 'B', 'end': 'D'},
                {'start': 'A', 'end': 'C', 'distance': 20},
                {'start': 'C', 'end': 'D', 'distance': 30},
                {'start': 'B', 'end': 'E', 'distance': 50},
                {'start': 'D', 'end': 'E', 'distance': 30},
            ],
        }
        return json.dumps(payload)

    def setup(self):
        self.url = reverse('core:map')

    def test_post_authorized_client(self, authorized_client, correct_payload):
        resp = authorized_client.post(self.url, correct_payload,
                                      content_type='application/json')
        assert resp.status_code == status.HTTP_201_CREATED

    def test_post_with_missing_data(self, authorized_client):
        resp = authorized_client.post(self.url, {},
                                      content_type='application/json')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_missing_fields(self, authorized_client,
                                      missing_fields_payload):
        resp = authorized_client.post(self.url,
                                      missing_fields_payload,
                                      content_type='application/json')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_authorized_client_and_persist_data(self, authorized_client,
                                                     correct_payload):
        resp = authorized_client.post(self.url, correct_payload,
                                      content_type='application/json')
        assert resp.status_code == status.HTTP_201_CREATED
        assert Map.objects.count() == 1
        assert Route.objects.count() == 6

    def test_post_same_request_twice(self, authorized_client,
                                     correct_payload):
        resp = authorized_client.post(self.url, correct_payload,
                                      content_type='application/json')
        assert resp.status_code == status.HTTP_201_CREATED

        resp = authorized_client.post(self.url, correct_payload,
                                      content_type='application/json')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        assert Map.objects.count() == 1
        assert Route.objects.count() == 6

    def test_get_all_maps(self, authorized_client):
        routes = mixer.cycle(6).blend(Route)
        mixer.blend(Map, routes=routes)
        resp = authorized_client.get(self.url,
                                     content_type='application/json')
        assert resp.status_code == status.HTTP_200_OK

    def test_get_without_maps_on_database(self, authorized_client):
        resp = authorized_client.get(self.url,
                                     content_type='application/json')
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestMapDetailView:

    def setup(self):
        self.routes = mixer.cycle(6).blend(Route)
        self.map = mixer.blend(Map, routes=self.routes)
        self.url = reverse('core:map_detail',
                           kwargs={'map_id': str(self.map.id)})

    def test_get_authorized_client(self, authorized_client):
        resp = authorized_client.get(self.url, content_type='application/json')
        assert resp.status_code == status.HTTP_200_OK

    def test_get_authorized_client_with_invalid_id(self, authorized_client):
        fake_uuid = str(uuid4())
        url = reverse('core:map_detail', kwargs={'map_id': fake_uuid})
        resp = authorized_client.get(url, content_type='application/json')
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestMapDetailShortPathView:

    def setup(self):
        self.routes = (
            mixer.blend(Route, start='A', end='B', distance=10),
            mixer.blend(Route, start='B', end='D', distance=15),
            mixer.blend(Route, start='A', end='C', distance=20),
            mixer.blend(Route, start='C', end='D', distance=30),
            mixer.blend(Route, start='B', end='E', distance=50),
            mixer.blend(Route, start='D', end='E', distance=30),
        )
        self.map = mixer.blend(Map, name='SP', routes=self.routes)
        self.url = reverse('core:map_detail_short_path',
                           kwargs={'map_id': str(self.map.id),
                                   'start': 'A',
                                   'end': 'D'})

    def test_get_authorized_client(self, authorized_client):
        resp = authorized_client.get(self.url, content_type='application/json')
        assert resp.status_code == status.HTTP_200_OK

    def test_get_authorized_client_with_invalid_id(self, authorized_client):
        fake_uuid = str(uuid4())
        url = reverse('core:map_detail_short_path',
                      kwargs={'map_id': fake_uuid,
                              'start': 'A',
                              'end': 'D'})
        resp = authorized_client.get(url, content_type='application/json')
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_get_authorized_client_content(self, authorized_client):
        resp = authorized_client.get(self.url, content_type='application/json')
        assert resp.json() == {'cost': Decimal('6.25'),
                               'path': ['A', 'B', 'D']}
