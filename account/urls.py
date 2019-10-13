from django.urls import path

#from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, handler500, handler404, handler403, handler400
from .views import * #LoginView, SignupView, ProfileView, PaymentOptionView, ChangePassView


urlpatterns = [
    url(r'^auth/join/$', SignupView.as_view(), name="signup"),          #ok
    url(r'^user/login$', LoginView.as_view(), name="login"),            #ok
    url(r'^user/logout$', LogoutView.as_view(), name="logout"),         #ok
    url(r'^account/profile$', ProfileView.as_view(), name='profile'),   #ok
    url(r'^account/email$', ChangeEmailView.as_view(), name='profile'), #ok
    url(r'^account/payment$', PaymentOptionView.as_view(), name='payment-management'),
    url(r'^account/password$', ChangePassView.as_view(), name='change-pass'), #ok
    url(r'^account/address$', UserAddressList.as_view(), name='user-address'), #ok
    url(r'^account/address/new$', UserNewAddressView.as_view(), name='user-new-address'), #ok
    url(r'^account/wallet$', LoyaltyPointView.as_view(), name='loyalty-bonus'), #ok
]
