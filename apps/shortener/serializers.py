from rest_framework import serializers
from apps.shortener.models import URL
from apps.shortener.utils import get_short_url, url_validator


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
        if value and url_validator(value):
            raise serializers.ValidationError(
                "custom short_url could not be URL itself.Please try for sequence of string instead of a valid URL!"
            )

        short_url = get_short_url(value)

        if URL.objects.filter(short_url=short_url).exists():
            raise serializers.ValidationError("url with this short url already exists.")
        return short_url

    # def create(self, validated_data):
    #     """
    #     Responsible to creating url object.
    #     Args:
    #         validated_data: validated clients input data
    #
    #     Returns:
    #         URL: and instance of the URL model.
    #     """
    #     url = URL.objects.create(
    #         **validated_data
    #     )
    #     return url


class UpdateURLSerializer(URLSerializer):
    class Meta:
        model = URLSerializer.Meta.model
        fields = URLSerializer.Meta.fields
        read_only_fields = ("created_at", "update_at",)
