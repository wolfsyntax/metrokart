from django.urls import path
from django.conf.urls import url, handler500, handler404, handler403, handler400
from .views import *

urlpatterns = [
    url(r'^auth/merchant/join$', MerchantCreateView.as_view(), name="merchant-form"),
    url(r'^dashboard$', DashboardView.as_view(), name="dashboard"),
    #url(r'^c/(?P<slug>[a-z\-]+)$', CategoryDetailView.as_view(), name="category-detail")
]
