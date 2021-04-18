from rest_framework import serializers
from apps.shortener.models import URL


class URLSerializer(serializers.ModelSerializer):

    class Meta:
        model = URL
        fields = "__all__"
        read_only_fields = ("short_url", "visit_count", "created_at", "update_at",)
