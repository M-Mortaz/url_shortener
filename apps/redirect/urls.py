from django.conf.urls import url
from apps.redirect import views

urlpatterns = [
    url(r'^(?P<short_url>[0-9a-zA-Z]+)/$', views.RedirectView.as_view(), name='redirect_v1'),
]
