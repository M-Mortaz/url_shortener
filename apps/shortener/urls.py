from django.conf.urls import url
from apps.shortener import views

urlpatterns = [
    url(r'^$', views.URLShortenerCreateListView.as_view(), name='url_shortener_view_CL'),
    url(r'^url/(?P<url_id>[0-9]+)/$', views.URLShortenerRetrieveUpdateDestroyView.as_view(), name='url_shortener_view_RUD'),
]
