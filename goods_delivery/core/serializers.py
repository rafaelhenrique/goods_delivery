from rest_framework import serializers

from .models import Map, Route


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('start', 'end', 'distance')


class MapListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)

    class Meta:
        model = Map
        fields = ('id', 'name')


class MapSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
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
        fields = ('id', 'name', 'routes')


class PathSerializer(serializers.Serializer):
    start = serializers.CharField(max_length=32)
    end = serializers.CharField(max_length=32)
    autonomy = serializers.DecimalField(max_digits=10, decimal_places=3)
    fuel_price = serializers.DecimalField(max_digits=10, decimal_places=3)

    def validate_start(self, value):
        """
        Check that the start value is a valid start route.
        """
        routes = Route.objects.filter(start=value)
        if not routes:
            raise serializers.ValidationError("start value not found.")
        return value

    def validate_end(self, value):
        """
        Check that the end value is a valid end route.
        """
        routes = Route.objects.filter(end=value)
        if not routes:
            raise serializers.ValidationError("end value not found.")
        return value
