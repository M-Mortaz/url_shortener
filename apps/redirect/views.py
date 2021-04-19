import logging

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from apps.shortener.models import URL
from apps.redirect.tasks import increasing_visit_url
from utils import set_url_details_redis, get_url_details_redis

logger = logging.getLogger(__name__)


class RedirectView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, short_url, *args, **kwargs):
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

        return redirect(original_url)
