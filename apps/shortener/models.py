from django.db import models
from apps.shortener.utils import create_random_string
from URLShortener.redis import redis_client
import logging

logger = logging.getLogger("__name__")


class URLManager(models.Manager):
    def create(self, **kwargs):
        url = kwargs.get("url")
        if not (url and isinstance(url, str)):
            raise ValueError(f"URL should be string.")
        short_url = URL.create_short_url()
        url_obj = self.model(
            short_url=short_url,
            **kwargs
        )
        url_obj.save(using=self._db)
        URL.add_url_to_redis(url=url, url_shortener=short_url)
        return url_obj


class URL(models.Model):
    original_url = models.URLField(db_index=True, unique=True)
    short_url = models.CharField(max_length=100, unique=True, db_index=True)
    visit_count = models.PositiveBigIntegerField(default=0)
    # creator = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = URLManager()
