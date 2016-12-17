from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class MapView(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        return Response({},
                        status=status.HTTP_201_CREATED)
