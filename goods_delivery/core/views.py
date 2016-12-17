from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MapSerializer
from .models import Map


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
