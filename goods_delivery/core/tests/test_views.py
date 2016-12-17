import json

import pytest
from django.core.urlresolvers import reverse
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
    def missing_data_payload(self):
        payload = {
            'name': 'Map01',
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

    def test_post_with_missing_data(self, authorized_client,
                                    missing_data_payload):
        resp = authorized_client.post(self.url,
                                      missing_data_payload,
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
