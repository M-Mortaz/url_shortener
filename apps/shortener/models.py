import logging

from django.db import models
from utils import set_url_details_redis, delete_url_details_redis

from URLShortener.redis import redis_client
from apps.shortener.utils import id_to_short_url

logger = logging.getLogger("__name__")


class URLManager(models.Manager):
    def create(self, **kwargs):
        url_obj = self.model(**kwargs)
        url_obj.save(using=self._db)
        url_obj.short_url = id_to_short_url(url_obj.id)
        url_obj.save()
        set_url_details_redis(
            original_url=url_obj.original_url,
            short_url=url_obj.short_url,
            url_id=url_obj.id
        )
        return url_obj


class URL(models.Model):
    original_url = models.URLField(db_index=True, unique=True)
    short_url = models.CharField(max_length=100, unique=True, db_index=True, default=None, null=True)
    visit_count = models.PositiveBigIntegerField(default=0)
    # creator = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = URLManager()
