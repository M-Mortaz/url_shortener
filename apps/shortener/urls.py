from django.conf.urls import url
from apps.shortener import views

urlpatterns = [
    url(r'^$', views.URLShortenerCreateListView.as_view(), name='url_shortener_view_CL'),
    url(r'^url/(?P<url_id>[0-9]+)/$', views.URLShortenerRetrieveUpdateDestroyView.as_view(), name='url_shortener_view_RUD'),
    url(r'^visit_count/url/(?P<url_id>[0-9]+)/$', views.RetrieveVisitCountIDView.as_view()),
    url(r'^visit_count/short/url/(?P<short_url>[0-9a-zA-Z]+)/$', views.RetrieveVisitCountURLView.as_view()),
]
