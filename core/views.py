from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, DeleteView
# Create your views here.
from core.models import *
from django.contrib.auth.models import User

import stripe
stripe.api_key = "sk_test_CoFwjEbDFLL9F1rr0MyVq5EH00nPqKFk1E"


from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

class CategoryDetailView(DetailView):

    template_name = "core/category_detail.html"
    #slug_field = "slug"
    #slug_url_kwarg = "slug"
    context_object_name = 'category_data'

    def get_queryset(self):
        category_data = Category.objects.filter(slug=self.kwargs['slug'])
        return  category_data
        #return Product.objects.filter(category_id=category_data[0].id)

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        context['data'] = Category.objects.filter(slug=self.kwargs['slug'])
        context['product_list'] = Product.objects.filter(category_id=context['data'][0].id)
        return context

class ProductDetailView(DetailView):

    template_name = "core/product_detail.html"
    #slug_field = "slug"
    #slug_url_kwarg = "slug"
    context_object_name = 'product_data'

    def get_queryset(self):

        return Product.objects.filter(slug=self.kwargs['slug'])
        #return Product.objects.filter(category_id=category_data[0].id)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        context['data'] = Product.objects.filter(slug=self.kwargs['slug'])
        #context['product_list'] = Product.objects.filter(category_id=context['data'][0].id)
        return context

class CoinBalanceView(TemplateView):

    template_name = "account/coinwallet.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CoinBalanceView, self).get_context_data(*args, **kwargs)

        user_data = RoyaltyBonus.objects.filter(user=self.request.user)

        total = 0.0

        for data in user_data:
            total += data.coin_earn

        context['record'] = user_data
        context['balance'] = total

        return context