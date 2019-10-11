from django import forms
from django.contrib.auth.models import User
from mall.models import Merchant

import re

class MerchantForm(forms.Form):

    last_name = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    email = forms.CharField(max_length=254)
    password = forms.CharField(max_length=30, error_messages={"required":"Password is required"}, help_text="Password must be a strong password")
    conf_password = forms.CharField(max_length=30, error_messages={"required":"Confirm Password is required."})

#    company_name = forms.CharField(max_length=100)
#    company_address = forms.CharField(max_length=255)
#    contact_name = forms.CharField(max_length=100)
#    contact_title = forms.CharField(max_length=100)
#    phone = forms.RegexField(regex="^(\+63|0)9[0-9]{9}$" ,max_length=13)

#    telephone = forms.CharField(max_length=100)
#    fax = forms.CharField(max_length=100)
#    company_logo = forms.ImageField()
#    payment_methods = forms.MultipleChoiceField()

#    can_shipped = forms.BooleanField()
#    tin = forms.RegexField(regex="^[\d]{3}-[\d]{3}-[\d]{3}-[\d]{3}$", max_length=15)
#    permit_no = forms.RegexField(regex="[a-zA-Z0-9]{8,}", max_length=32)

    def clean(self):
        cd = super(MerchantForm, self).clean()
        password = self.cleaned_data['password']
        conf_password = self.cleaned_data['conf_password']

        # (?=.*[a-hj-np-z])(?=.*[A-HJ-NP-Z])(?=.*(\d|!0)).{8,}

        if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*[2-9])(?=.*(_|[^\w])).{8,}$', password):
            self.add_error('password', 'Password must contains alpha-numeric and special characters.')

        if len(password) < 8:
            self.add_error('password', 'Password must contains at least eight (8) alpha-numeric and special characters.')

        if password != conf_password:
            self.add_error('conf_password', 'Confirm Password not match.')

        return cd

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email', '')
        print("\n\n\nValidating Email address\n\n\n")
        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)

        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This Email address is already in use.')

    def clean_username(self):
        # Get the email
        uname = self.cleaned_data.get('username', '')

        try:
            match = User.objects.get(username=uname)

        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return uname

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('Username is already in use.')

    def save(self, args=False):

        cd = self.cleaned_data
        #username = cd['email'].split("@")[0]
        print("\n\n\n\n\n\n\n\nSaving Data:\n{}\n\n\n\n\n\n\n\n\n\n".format(cd))

        userdata = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])

        userdata.first_name = cd['first_name']
        userdata.last_name = cd['last_name']
        userdata.is_staff = True

        userdata.is_active = False

        userdata.save()
