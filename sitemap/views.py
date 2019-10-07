from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from core.models import Category
from datetime import datetime

# Create your views here.
class HomeView(ListView):

    #template_name = "account/change_phone.html"
    template_name = "sitemap/index.html"
    paginate_by = 10
    queryset = [Category.objects.filter(status=True), ]
    context_object_name = 'records'

    def get_context_data(self, *args, **kwargs):

        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['category'] = Category.objects.filter(status=True)
        #context['now'] = datetime.now()

        return context
