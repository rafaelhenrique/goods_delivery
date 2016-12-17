import pytest
from mixer.backend.django import mixer
from django.db import IntegrityError
from goods_delivery.core.models import Route, Map


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
