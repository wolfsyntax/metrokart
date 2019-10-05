from django.urls import path
from django.conf.urls import url, handler500, handler404, handler403, handler400
from .views import *

urlpatterns = [
    url(r'^user/coin/$', CoinBalanceView.as_view(), name="coin-wallet"),
    url(r'^c/(?P<slug>[a-z\-]+)$', CategoryDetailView.as_view(), name="category-detail")
]
