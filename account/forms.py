from django import forms

from django.contrib.auth.models import User

from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives

from django.template.loader import get_template, render_to_string

from django.contrib.auth import update_session_auth_hash


import re   # Regular Expression
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('C', 'Custom'),
)

class UserRegistrationForm(forms.Form):

    email = forms.EmailField(max_length=254, error_messages={"required": "Email is required."})
    username = forms.CharField(max_length=64, error_messages={"required":"Username is required."})
    first_name = forms.RegexField(regex="^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$", max_length=64, error_messages={"required": "First name is required."})
    last_name = forms.RegexField(regex="^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$", max_length=64, error_messages={"required":"Last name is required"})
    password = forms.CharField(max_length=30, error_messages={"required":"Password is required"}, help_text="Password must be a strong password")
    conf_password = forms.CharField(max_length=30, error_messages={"required":"Confirm Password is required."})
    phone = forms.RegexField(regex=r"^(\+63|0)9[0-9]{9}$", max_length=13, error_messages={"invalid":"Phone number is invalid format","required": "Mobile Phone is required."})
    gender = forms.MultipleChoiceField(choices=GENDER)
    birthdate = forms.DateField()

    def clean(self):
        cd = super(UserRegistrationForm, self).clean()
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

        userdata = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])

        userdata.first_name = cd['first_name']
        userdata.last_name = cd['last_name']
        userdata.is_staff = args

        if args:
            userdata.is_active = False

        userdata.save()

       # print("\n\nData successfully save!\n\n")
