import logging

from django.db import models

from URLShortener.redis import redis_client
from apps.shortener.utils import create_short_url

logger = logging.getLogger("__name__")


class URLManager(models.Manager):
    def create(self, **kwargs):
        orig_url = kwargs.get("original_url")
        if not (orig_url and isinstance(orig_url, str)):
            raise ValueError(f"URL should be string.")

        url_obj = self.model(**kwargs)
        url_obj.save(using=self._db)

        URL.add_url_to_redis(url=orig_url, url_shortener=kwargs.get("short_url"))

        return url_obj


class URL(models.Model):
    original_url = models.URLField(db_index=True, unique=True)
    short_url = models.CharField(max_length=100, unique=True, db_index=True, default=create_short_url)
    visit_count = models.PositiveBigIntegerField(default=0)
    # creator = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = URLManager()

    @staticmethod
    def add_url_to_redis(url: str, url_shortener: str) -> None:
        """
        Adding original and short URL to the redis for better performance on the redirect part.

        Note:
            Since this method responsible for increasing performance, if any error occurs we just log it as a warning
             and not raising any error/exception.
        Args:
            url: original url
            url_shortener: short url

        Returns:
            None

        Raises:
            None
        """
        try:
            if redis_client.get(url_shortener) is None:
                redis_client.set(url_shortener, url)
        except Exception as e:
            logger.warning(f"The error occurs in the redis during adding url. the error is {e}")
