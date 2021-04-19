from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.db.models import F

from apps.shortener.models import URL


@shared_task
def increasing_visit_url(url_id):
    URL.objects.filter(id=url_id).update(visit_count=F("visit_count") + 1)
