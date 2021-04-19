from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.shortener.serializers import URLSerializer, UpdateURLSerializer
import logging
from apps.shortener.models import URL
from utils import set_url_details_redis, delete_url_details_redis

logger = logging.getLogger()


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

    def get_serializer_context(self):
        return {"url_id": self.kwargs["url_id"]}

    def perform_update(self, serializer):
        url = serializer.save()
        set_url_details_redis(
            original_url=url.original_url,
            short_url=url.short_url,
            url_id=url.id
        )

    def perform_destroy(self, instance):
        instance.delete()
        delete_url_details_redis(short_url=instance.short_url)
