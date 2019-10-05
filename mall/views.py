from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView

from .forms import MerchantForm

# Create your views here.
class MerchantCreateView(CreateView):

    form_class = MerchantForm
    template_name = "mall/mall_create.html"

    #def form_valid(self, form):

    #    self.object = form.save(commit=False)
    #    self.object.user = self.request.user
    #    self.object.save()
    #    return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        context = {
            'form' : MerchantForm
        }

        return render(request, "mall/mall_create.html", context)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))