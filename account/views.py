from django.shortcuts import render, HttpResponseRedirect

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login
from django.views.generic import TemplateView, CreateView, RedirectView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import  messages

from .forms import UserRegistrationForm


class LoginView(TemplateView):

    template_name = "account/login.html"
    #success_url = "auth/join/" # None
    redirect_authenticated_user = True
    redirect_field_name = 'next'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self, request, *args, **kwargs):
       # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        #print("\n\n\nUsername: {}\n\n\n".format(request.POST["username"]))
        #return HttpResponse("LOGIN ATTEMPT")
        username =  request.POST["username"]
        password = request.POST["password"]

        userdata = authenticate(username=username, password=password)

        if not userdata is None:

            print("\n\n\n\nuser exist")

            if userdata.is_active :
                login(request, userdata)

                if userdata.is_superuser or userdata.is_staff:

                    return HttpResponseRedirect("/admin/")

                else:

                    return HttpResponseRedirect("/")


        else:
           # print("\n\n\nuser doesn't exist")
            messages.add_message(request,messages.ERROR, "Invalid Username or Password")

        return render(request, "account/login.html")

class LogoutView(RedirectView):

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        next_page = "/"
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)

        return super().dispatch(request, *args, **kwargs)


class SignupView(TemplateView):

    template_name = "account/register.html"
    form_class = UserRegistrationForm

    def post(self, request):
        form = self.form_class(request.POST)
        print("\n\n\n\nSignup View Submission\n\n\n\n")
        if form.is_valid():
            print("\n\n\n\nForm is valid\n\n\n\n")
            form.save()

            return HttpResponseRedirect('/user/login?next=/')
        return render(request, self.template_name, {"form": form})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        return context

class PaymentOptionView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"

class UserAddressView(LoginRequiredMixin, TemplateView):
    template_name = "account/new_address.html"

class UserNewAddressView(LoginRequiredMixin, TemplateView):
    template_name = "account/new_address.html"


class ChangePassView(LoginRequiredMixin, TemplateView):
    template_name = "account/change_password.html"

class ChangeEmailView(LoginRequiredMixin, TemplateView):
    template_name = "account/change_email.html"

class ChangePhoneView(LoginRequiredMixin, TemplateView):
    template_name = "account/change_phone.html"

class LoyaltyPointView(LoginRequiredMixin, TemplateView):
    template_name = "account/coinwallet.html"

class VoucherView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"

class NotificationView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"

class PurchaseView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"
