from django.db import models
from django.conf import settings
from urllib import parse
from apps.shortener.utils import create_random_string
from URLShortener.redis import redis_client
import logging

logger = logging.getLogger("__name__")


class URLManager(models.Manager):
    def create(self, **kwargs):
        base_domain = settings.BASE_DOMAIN
        orig_url = kwargs.get("original_url")
        if not (orig_url and isinstance(orig_url, str)):
            raise ValueError(f"URL should be string.")
        short_url = URL.create_short_url()
        url_obj = self.model(
            short_url=parse.urljoin(base_domain, short_url),
            **kwargs
        )
        url_obj.save(using=self._db)
        URL.add_url_to_redis(url=orig_url, url_shortener=short_url)
        return url_obj


class URL(models.Model):
    original_url = models.URLField(db_index=True, unique=True)
    short_url = models.CharField(max_length=100, unique=True, db_index=True)
    visit_count = models.PositiveBigIntegerField(default=0)
    # creator = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = URLManager()

    @staticmethod
    def create_short_url() -> str:
        """
        Create short url from original url.
        Note: This method will try for 5 times in a row to create a 5-character pass that is unique and does not exist
         in the database. If the unique pass is not generated in these 5 times, it will try to generate 6, 7, and 8 to
         100 characters next time.
        Returns:
            str: short url.
        Raises:
            Exception: If all of our try for generating unique url failed.This raise it is not possible in the normal
             situation
        """
        # import hashlib
        # return hashlib.sha1(url.encode("UTF-8")).hexdigest()[:settings.SHORTENER_MIN_HASH_LENGTH]
        for _ in range(100):
            for i in range(5):
                short_url = create_random_string(i)
                if not URL.objects.filter(short_url=short_url).exists():
                    # we achieved to our short url so exit from method and loop.
                    return short_url
        else:
            raise Exception(f"It is not possible to create unique short URL!")

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
