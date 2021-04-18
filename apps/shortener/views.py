from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.shortener.serializers import URLSerializer, UpdateURLSerializer
from apps.shortener.models import URL


class URLShortenerCreateListView(generics.ListCreateAPIView):
    """
    submit new short url, get list of all urls detail.
    using default pagination for post method.
    """
    # TODO: @security -> be care for following permission and change it to appropriate permission level.
    permission_classes = (AllowAny, )
    serializer_class = URLSerializer
    queryset = URL.objects.all()


class URLShortenerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update and Destroy the URL object using generic DRF view. simple and secure :)
    # TODO: @security -> be care for following permission and change it to appropriate permission level.
    """
    permission_classes = (AllowAny,)
    serializer_class = UpdateURLSerializer
    queryset = URL.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "url_id"
