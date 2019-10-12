from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, TemplateView

from .forms import MerchantForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

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

            return HttpResponseRedirect('/user/login?next=/')
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


    def get_context_data(self, **kwargs):

        context = super(DashboardView, self).get_context_data(**kwargs)
        #context['form'] = self.form_class

        return context