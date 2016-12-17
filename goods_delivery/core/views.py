from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Map
from .serializers import MapListSerializer, MapSerializer


class MapView(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = MapSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        maps = Map.objects.all()
        if not maps:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MapListSerializer(maps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MapDetailView(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, map_id):
        try:
            map_object = Map.objects.get(id=map_id)
            serializer = MapSerializer(map_object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Map.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
