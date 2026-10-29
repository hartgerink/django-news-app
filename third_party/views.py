"""
The simulated third party's API: the endpoint that receives approved
articles.
"""

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import ThirdPartyArticleSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def receive_article(request):
    """
    The simulated third party's endpoint, which receives approved
    articles as JSON and saves them.

    The third party expects a valid API key in the ``X-API-Key``
    header, checked against the ``THIRD_PARTY_API_KEY`` setting. The
    view checks the key itself, so the usual login and permission
    checks of Django REST Framework (DRF) are turned off. A request
    without the right API key, or with missing or invalid fields, is
    refused with a message saying why.

    :param request: The API request, with the article as JSON.
    :returns: 201 Created, with the saved article; 401 Unauthorized if
        the API key is missing or not valid; or 400 Bad Request, with
        each missing or invalid field.
    """
    sent_key = request.headers.get("X-API-Key")
    if sent_key is None:
        return Response(
            {"detail": "The X-API-Key header is missing."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if sent_key != settings.THIRD_PARTY_API_KEY:
        return Response(
            {"detail": "The API key is not valid."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    serializer = ThirdPartyArticleSerializer(data=request.data)
    if not serializer.is_valid():
        # The errors list each missing or invalid field.
        return Response(
            {
                "detail": "Some fields are missing or not valid.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer.save()
    return Response(
        {"detail": "The article was received.", "article": serializer.data},
        status=status.HTTP_201_CREATED,
    )
