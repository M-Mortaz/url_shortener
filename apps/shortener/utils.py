import string, random
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
