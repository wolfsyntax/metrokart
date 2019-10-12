from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, TemplateView

from .forms import MerchantForm, MerchantUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Merchant

# Create your views here.
class MerchantCreateView(TemplateView):

    form_class = MerchantForm
    template_name = "mall/mall_create.html"

    def get_context_data(self, **kwargs):

        context = super(MerchantCreateView, self).get_context_data(**kwargs)
        context['form'] = self.form_class

        return context

    def post(self, request):
        form = self.form_class(request.POST)
        print("\n\n\n\nSignup View Submission\n\n\n\n")
        if form.is_valid():
            print("\n\n\n\nForm is valid\n\n\n\n")
            form.save()

            return HttpResponseRedirect('/user/login?next=/dashboard')
        return render(request, self.template_name, {"form": form})
    #def form_valid(self, form):

    #    self.object = form.save(commit=False)
    #    self.object.user = self.request.user
    #    self.object.save()
    #    return HttpResponseRedirect(self.get_success_url())

#    def get(self, request, *args, **kwargs):
#        context = {
#            'form' : MerchantForm
#        }

#        return render(request, "mall/mall_create.html", context)

#    def form_invalid(self, form):
#        return self.render_to_response(self.get_context_data(form=form))

class DashboardView(LoginRequiredMixin, TemplateView):

#    form_class = MerchantForm
    template_name = "mall/dashboard.html"

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_staff:
            raise PermissionDenied

        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        try:
            match = Merchant.objects.get(user_id=request.user.id)

        except Merchant.DoesNotExist:
            # Unable to find a user, this is fine
            print("Merchant Doesn't exist")
            return HttpResponseRedirect("/merchant/profile")

    def get_context_data(self, **kwargs):
        print("\n\n\n\n\n\n\n\n\n\n\nContext: {}\n\n\n\n\n\n".format(kwargs['request']))
        context = super(DashboardView, self).get_context_data(**kwargs)
        #context['form'] = self.form_class

        return context


class MerchantUpdateView(LoginRequiredMixin, TemplateView):

    form_class = MerchantUpdateForm
    template_name = "mall/merchant_profile.html"

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_staff:
            raise PermissionDenied

        return super(MerchantUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/dashboard')
        return render(request, self.template_name, {"form": form})

    def get_context_data(self, **kwargs):

        context = super(MerchantUpdateView, self).get_context_data(**kwargs)
        context['form'] = self.form_class

        return context

