from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.shortener.serializers import URLSerializer
from apps.shortener.models import URL


class URLShortenerCreateListView(generics.ListCreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = URLSerializer
    queryset = URL


class URLShortenerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    pass
