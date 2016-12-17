import json

import pytest
from django.core.urlresolvers import reverse
from rest_framework import status


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

    def test_post_authorized_client(self, authorized_client, correct_payload):
        resp = authorized_client.post(reverse('core:map'), correct_payload,
                                      content_type='application/json')
        assert resp.status_code == status.HTTP_201_CREATED
