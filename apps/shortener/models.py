from django.db import models


class URL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=100, unique=True)
    visit_count = models.PositiveBigIntegerField(default=0)
    # creator = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_Add=True)
    update_at = models.DateTimeField(auto_now=True)
