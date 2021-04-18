import random
import string
from urllib import parse

from django.conf import settings


def create_random_string(inc: int = 0) -> str:
    """
    create random string. the length depends on the input argument inc. the minimum length will be set to
     the SHORTENER_MIN_HASH_LENGTH variable in the django settings or environments variable.
    Args:
        inc (int): Excess amount over the minimum length of the shortener min hash length.
    Returns:
        str: a string with `default_min_length+inc` character sequence
    """
    sequence = string.ascii_letters + string.digits
    return ''.join(random.choices(sequence, k=settings.SHORTENER_MIN_HASH_LENGTH + inc))


def get_short_url(client_custom_short_url: str = None) -> str:
    """
    This function will choose we need create a sequence of string for shorted url or not.
    if the client send us a short url itself so we don't need to generate it.
    Args:
        client_custom_short_url(str|None): The custom clients suffix shorted url.

    Returns:
        str: valid shorted_url which joined based url and shorted url together.
    """
    return __create_short_url(client_custom_short_url) if client_custom_short_url else create_short_url()


def create_short_url() -> str:
    """
    Create unique short url.
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
    from apps.shortener.models import URL
    for _ in range(100):
        for i in range(5):
            short_url = create_random_string(i)
            if not URL.objects.filter(short_url=short_url).exists():
                # we achieved to our short url so exit from method and loop.
                return __create_short_url(short_url=short_url)
    else:
        raise Exception(f"It is not possible to create unique short URL!")


def __create_short_url(short_url: str) -> str:
    """
    Attaching the short url to the default domain.
    Args:
        short_url(str): a shorted url.

    Returns:
        str: valid short_url.
    """
    base_domain = settings.BASE_DOMAIN
    return parse.urljoin(base_domain, short_url)


def url_validator(url: str) -> bool:
    """
    check if the string is valid url or not.

    Args:
        url(str): input string which will check for url validation

    Returns:
        bool : True if url is valid otherwise False.
    """
    import re
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None
