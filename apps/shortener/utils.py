import string, random
from django.conf import settings


def create_random_string(inc: int = 0) -> str:
    """
    create random string.
    inc: Excess amount over the minimum length of the shortener min hash length.
    """
    sequence = string.ascii_letters + string.digits
    return ''.join(random.choices(sequence, k=settings.SHORTENER_MIN_HASH_LENGTH + inc))
