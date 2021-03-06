"""metrokart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from sitemap.views import *
from core.views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(("account.urls","account")), name="account"),
    url(r'^', include(("sitemap.urls","sitemap")), name="sitemap"),
    url(r'^', include(("core.urls","core")), name="core"),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^', include(("mall.urls","mall")), name="merchant"),
    url(r'test', TemplateView.as_view(template_name="mall/index.html"), name="test"),
    url(r'terms/merchant', TemplateView.as_view(template_name="sitemap/mall_terms.html"), name="terms-mall"),
    url(r'terms/customer', TemplateView.as_view(template_name="sitemap/client_terms.html"), name="terms-client"),
    url(r'docs/privacy', TemplateView.as_view(template_name="sitemap/privacy.html"), name="doc-privacy"),
    url(r'docs/policy/data', TemplateView.as_view(template_name="sitemap/data_policy.html"), name="data-policy"),
    url(r'docs/policy/cookies', TemplateView.as_view(template_name="sitemap/cookies_policy.html"), name="cookies-policy"),

]


