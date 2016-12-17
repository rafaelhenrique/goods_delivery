from rest_framework import serializers

from .models import Map, Route


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('start', 'end', 'distance')


class MapSerializer(serializers.ModelSerializer):
    routes = RouteSerializer(many=True)

    def create(self, validated_data):
        data_routes = validated_data.pop('routes')
        map_object = Map.objects.create(**validated_data)
        for data_route in data_routes:
            route, _ = Route.objects.get_or_create(**data_route)
            map_object.routes.add(route)
        return map_object

    class Meta:
        model = Map
        fields = ('name', 'routes')