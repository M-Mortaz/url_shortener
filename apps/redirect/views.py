from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apps.shortener.models import URL
from django.shortcuts import redirect
from utils import set_url_details_redis, get_url_details_redis
from apps.redirect.tasks import increasing_visit_url
from URLShortener.redis import redis_client
import logging
from django.shortcuts import get_object_or_404
import json


logger = logging.getLogger(__name__)


class RedirectView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, short_url, *args, **kwargs):
        # init values
        original_url = None
        original_url_id = None

        ####### Fetch original url from redis #######
        original_url, original_url_id = get_url_details_redis(short_url=short_url)
        #############################################

        ####### Fetch original url from DB if original url not exists in the redis ####
        if not (original_url and original_url_id):
            # if the url not exists in the DB then the 404 error will be raise.
            original_url_db = get_object_or_404(URL, short_url=short_url)
            original_url = original_url_db.original_url
            original_url_id = original_url_db.id
            # set original url related to short_url to redis for future
            set_url_details_redis(
                original_url=original_url,
                short_url=short_url,
                url_id=original_url_id
            )

        increasing_visit_url.delay(url_id=original_url_id)
        from django.db.models import F

        URL.objects.filter(id=original_url_id).update(visit_count=F("visit_count") + 1)

        return redirect(original_url)
