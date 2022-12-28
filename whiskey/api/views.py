from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.renderers import JSONRenderer


class BottlesApi(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        return Response({
            "bottles": [
                {"name": "Laphroig Quarter Cask", "kind": "whiskey"},
                {"name": "Bowmore 15", "kind": "whiskey"},
                {"name": "Ron Aldea Tradición", "kind": "rum"},
            ]
        })

