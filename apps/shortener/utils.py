import random
import string


def id_to_short_url(id):
    map = string.ascii_letters + string.digits
    short_url = ""

    # for each digit find the base 62
    while id > 0:
        short_url += map[id % 62]
        id //= 62

    # reversing the shortURL
    return short_url[len(short_url):: -1]


def short_url_to_id(short_url):
    id = 0
    for i in short_url:
        val_i = ord(i)
        if ord('a') <= val_i <= ord('z'):
            id = id * 62 + val_i - ord('a')
        elif ord('A') <= val_i <= ord('Z'):
            id = id * 62 + val_i - ord('Z') + 26
        else:
            id = id * 62 + val_i - ord('0') + 52
    return id


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
