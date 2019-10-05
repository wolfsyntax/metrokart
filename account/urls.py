from django.urls import path

#from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, handler500, handler404, handler403, handler400
from .views import * #LoginView, SignupView, ProfileView, PaymentOptionView, ChangePassView


urlpatterns = [
    url(r'^auth/join/$', SignupView.as_view(), name="signup"),
    url(r'^user/login$', LoginView.as_view(), name="login"),
    url(r'^user/logout$', LogoutView.as_view(), name="logout"),
    url(r'^account/profile$', ProfileView.as_view(), name='profile'),
    url(r'^account/email$', ChangeEmailView.as_view(), name='profile'),
    url(r'^account/payment$', PaymentOptionView.as_view(), name='payment-management'),
    url(r'^account/password$', ChangePassView.as_view(), name='change-pass'),
    url(r'^account/address$', UserAddressView.as_view(), name='user-address'),
    url(r'^account/wallet$', LoyaltyPointView.as_view(), name='loyalty-bonus'),
]
