import logging

from rest_framework import serializers

from apps.shortener.models import URL
from apps.shortener.utils import url_validator
from utils import set_url_details_redis, delete_url_details_redis

logger = logging.getLogger(__name__)


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = "__all__"
        read_only_fields = ("visit_count", "created_at", "update_at",)

    def validate_short_url(self, value: str) -> str:
        """
        Check short_url field validation. Since this filed is too complex we implement a custom validation for it.

        Args:
            value(str|None): clients custom input value for url.

        Returns:
            str: Validate short_url
        """
        url_id = self.context.get("url_id")  # just in update mode we have id.

        if url_id:  # for update step old and new short_value could be same.
            try:
                old_short_url = URL.objects.get(id=url_id).short_url
            except URL.DoesNotExist:
                raise serializers.ValidationError("url does not exists!")
            if old_short_url == value:
                return value

        if value and url_validator(value):
            raise serializers.ValidationError(
                "custom short_url could not be URL itself.Please try for sequence of string instead of a valid URL!"
            )

        if URL.objects.filter(short_url=value).exists():
            raise serializers.ValidationError("url with this short url already exists.")
        return value


class UpdateURLSerializer(URLSerializer):
    class Meta:
        model = URLSerializer.Meta.model
        fields = URLSerializer.Meta.fields
        read_only_fields = ("created_at", "update_at",)

