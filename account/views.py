from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied

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
from account.models import UserProfile, Address
from .forms import UserRegistrationForm, ChangeEmailForm, ChangePassForm, UserProfileForm, UserAddressForm

from django.contrib.auth.hashers import make_password, check_password


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

                if userdata.is_superuser:
                    
                    print("\n\n\n\n\Admin\n\n\n\n")
                    return HttpResponseRedirect("/admin/")

                elif userdata.is_staff:
                    
                    print("\n\n\n\n\Merchant\n\n\n\n")
                    return HttpResponseRedirect("/dashboard")

                else:
                    
                    print("\n\n\n\n\Customer\n\n\n\n")
                    return HttpResponseRedirect("/")

            #else:
                #messages.add_message(request, messages.ERROR, "Inactive account")
        else:
           # print("\n\n\nuser doesn't exist")
            messages.add_message(request,messages.ERROR, "Inactive or Invalid credentials")

        return render(request, "account/login.html")

class LogoutView(RedirectView):

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        next_page = "/"
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)

        return super(LogoutView, self).dispatch(request, *args, **kwargs)


class SignupView(TemplateView):

    template_name = "account/register.html"
    form_class = UserRegistrationForm

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            form.save()

            messages.add_message(request, messages.SUCCESS, "Account has been created successfully!!!")

            return HttpResponseRedirect('/user/login?next=/')

        return render(request, self.template_name, {"form": form})

class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "account/profile.html"
    form_class = UserProfileForm

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_staff:
            raise PermissionDenied

        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():

            if form.save(request.user.id):
                return HttpResponseRedirect("/")
            else:
                messages.add_message(request, messages.WARNING, "Please enter the current password!"
                                     )
        return render(request, self.template_name, {"form": form})

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        return context

class PaymentOptionView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"

class UserAddressList(LoginRequiredMixin, TemplateView):

    template_name = "account/address_list.html"
#    form_class = UserAddressForm

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_staff:
            raise PermissionDenied

        self.userid = request.user.id

        return super(UserAddressList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(UserAddressList, self).get_context_data(**kwargs)



        try:
            d = Address.objects.filter(user_id=self.userid)

            print("\n\n\n\nThis user #{} is requesting to access this module\n\n\n".format(self.userid))
            #print("This is the record: {}\n\n".format(d.consignee))

            context['address_list'] = d
            context['address_list_total'] = d.count()
            #data = Address.objects.get(user_id=self.userid)
            #context['address_list'] = data
            #print("\n\n\nUser Address\n\n{}\n\n\n\n\n".format(data))

        except Address.DoesNotExist:
            pass


        return context


class UserNewAddressView(LoginRequiredMixin, TemplateView):

    template_name = "account/new_address.html"
    form_class = UserAddressForm

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_staff:
            raise PermissionDenied

        return super(UserNewAddressView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(UserNewAddressView, self).get_context_data(**kwargs)

        context['form'] = self.form_class

        return context

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        print("\n\n\nUserNewAddressView POST\n\n\n")
        if form.is_valid():
            print("UserNewAddressView ValidForm\n\n\n")

            if form.save(request.user.id):
                return HttpResponseRedirect("/account/address")

        return render(request, self.template_name, {"form": form})

class ChangePassView(LoginRequiredMixin, TemplateView):
    template_name = "account/change_password.html"
    form_class = ChangePassForm

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_staff:
            raise PermissionDenied

        return super(ChangePassView, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():

            if form.save(request.user.id):
                return HttpResponseRedirect("/account/profile")
            else:
                messages.add_message(request, messages.WARNING, "Please enter the current password!"
                                     )
        return render(request, self.template_name, {"form": form})



class ChangeEmailView(LoginRequiredMixin, TemplateView):
    template_name = "account/change_email.html"
    form_class = ChangeEmailForm

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_staff:
            raise PermissionDenied

        return super(ChangeEmailView, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        form = self.form_class(request.POST)

        #cd = form.clean()
        #print("\n\n\n\nRequesting to change Email Address\n\n\n\n\nCurrent Email: {}\nNew Email: {}\n\n\n\n\n".format(request.user.email, cd['email']))
        print("\n\n\n\nForm is valid: {}\n\n\n\n\n".format(form.is_valid()))


        if form.is_valid():

            if form.save(request.user.email):
                return HttpResponseRedirect("/account/profile")
            else:
                messages.add_message(request, messages.WARNING, "Please enter the current password!"
                                     )
        return render(request, self.template_name, {"form": form})



class ChangePhoneView(LoginRequiredMixin, TemplateView):
    template_name = "account/change_phone.html"

class LoyaltyPointView(LoginRequiredMixin, TemplateView):

    template_name = "account/coinwallet.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_staff:

            raise PermissionDenied
        else:
            self.userid = request.user.id

        return super(LoyaltyPointView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(LoyaltyPointView, self).get_context_data(**kwargs)
        context['loyalty_point'] = UserProfile.objects.get(user_id=self.userid).loyalty_point
        context['loyalty_trx'] = None

        return context

class VoucherView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"

class NotificationView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"

class PurchaseView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"
