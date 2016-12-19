import pytest
from django.db import IntegrityError
from mixer.backend.django import mixer

from goods_delivery.core.models import Map, Route


@pytest.mark.django_db
class TestRoute(object):
    """
    Run tests on Route model
    """
    def setup(self):
        self.route = mixer.blend(Route)

    @pytest.mark.parametrize('data', [
        {'start': None},
        {'end': None},
        {'distance': None},
    ])
    def test_required_fields(self, data):
        with pytest.raises(IntegrityError):
            Route.objects.update(**data)

    def test_str(self):
        assert isinstance(str(self.route), str)

    def test_repr(self):
        assert isinstance(repr(self.route), str)


@pytest.mark.django_db
class TestMap(object):
    """
    Run tests on Map model
    """
    def setup(self):
        self.map = mixer.blend(Map)

    @pytest.mark.parametrize('data', [
        {'name': None},
    ])
    def test_required_fields(self, data):
        with pytest.raises(IntegrityError):
            Map.objects.update(**data)

    def test_str(self):
        assert isinstance(str(self.map), str)

    def test_repr(self):
        assert isinstance(repr(self.map), str)

    def test_map_relations(self):
        route_01 = Route(start='A', end='B', distance=10)
        route_01.save()
        route_02 = Route(start='B', end='D', distance=15)
        route_02.save()

        map_object = Map(name='Map01')
        map_object.save()
        map_object.routes.add(route_01)
        map_object.routes.add(route_02)
        map_object.save()

        assert map_object.routes.count() == 2
        assert route_01.maps.count() == 1

        assert route_01.maps.first() == route_02.maps.first() == map_object
        assert map_object.routes.first().start == 'B'
        assert map_object.routes.last().start == 'A'

    def test_short_path(self):
        routes = (
            mixer.blend(Route, start='A', end='B', distance=10),
            mixer.blend(Route, start='B', end='D', distance=15),
            mixer.blend(Route, start='A', end='C', distance=20),
            mixer.blend(Route, start='C', end='D', distance=30),
            mixer.blend(Route, start='B', end='E', distance=50),
            mixer.blend(Route, start='D', end='E', distance=30),
        )
        map_ = mixer.blend(Map, name='SP', routes=routes)
        short_path, lenght = map_.short_path(start='A', end='D')
        assert short_path == ['A', 'B', 'D']
        assert lenght == 25
