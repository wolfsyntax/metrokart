from django.urls import path
from django.conf.urls import url, handler500, handler404, handler403, handler400
from .views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
]
