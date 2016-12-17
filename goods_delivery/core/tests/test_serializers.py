import pytest
from goods_delivery.core.serializers import RouteSerializer, MapSerializer
from goods_delivery.core.models import Route, Map


@pytest.mark.django_db
class TestRouteSerializer(object):
    """
    Run tests on RouteSerializer
    """
    def test_validated_data(self):
        data = {'start': 'A', 'end': 'B', 'distance': 10}
        serializer = RouteSerializer(data=data)
        assert serializer.is_valid()

    def test_save_data_using_serializer(self):
        data = {'start': 'A', 'end': 'B', 'distance': 10}
        serializer = RouteSerializer(data=data)
        serializer.is_valid()
        route = serializer.save()
        assert isinstance(route, Route)


@pytest.mark.django_db
class TestMapSerializer(object):
    """
    Run tests on MapSerializer
    """

    @pytest.fixture
    def correct_data(self):
        data = {
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
        return data

    def test_validated_data(self, correct_data):
        serializer = MapSerializer(data=correct_data)
        assert serializer.is_valid()

    def test_save_data_using_serializer(self, correct_data):
        serializer = MapSerializer(data=correct_data)
        serializer.is_valid()
        map_object = serializer.save()
        assert isinstance(map_object, Map)

    def test_data_content_saved_using_serializer(self, correct_data):
        expected_routes = (('D', 'E', 30), ('B', 'E', 50), ('C', 'D', 30),
                           ('A', 'C', 20), ('B', 'D', 15), ('A', 'B', 10))
        serializer = MapSerializer(data=correct_data)
        serializer.is_valid()
        map_object = serializer.save()
        routes = map_object.routes.all()

        assert map_object.name == 'Map01'
        assert routes.count() == 6
        for route in routes:
            assert (route.start, route.end, route.distance) in expected_routes
