from django.conf.urls import url
from apps.shortener import views

urlpatterns = [
    url(r'^$', views.URLShortenerCreateListView.as_view(), name='url_shortener_view'),
]
