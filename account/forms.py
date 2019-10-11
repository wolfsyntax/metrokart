from django import forms

from django.contrib.auth.models import User

from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives

from django.template.loader import get_template, render_to_string

from django.shortcuts import get_object_or_404

from django.contrib.auth import update_session_auth_hash

from .models import UserProfile

import re   # Regular Expression
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('C', 'Custom'),
)


class ChangeEmailForm(forms.Form):

    email = forms.EmailField(max_length=254, error_messages={"required": "Email is required."})
    password = forms.CharField(max_length=30, error_messages={"required":"Password is required"}, help_text="Password must be a strong password")

    def clean(self):
        cd = super(ChangeEmailForm, self).clean()
        password = self.cleaned_data['password']

        # (?=.*[a-hj-np-z])(?=.*[A-HJ-NP-Z])(?=.*(\d|!0)).{8,}

        if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*[2-9])(?=.*(_|[^\w])).{8,}$', password):
            self.add_error('password', 'Password must contains alpha-numeric and special characters.')

        if len(password) < 8:
            self.add_error('password', 'Password must contains at least eight (8) alpha-numeric and special characters.')


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

    def save(self, current_email):

        cd = self.cleaned_data
        userdata = User.objects.get(email=current_email)

        if userdata.check_password(cd['password']):

            userdata.email = cd['email']
            userdata.save()

            return True

        else:

            return False


class ChangePassForm(forms.Form):

    current_password = forms.CharField(max_length=30, error_messages={"required": "Current Password is required"},help_text="Current Password must be a strong password")
    password = forms.CharField(max_length=30, error_messages={"required": "Password is required"},help_text="New Password must be a strong password")
    conf_password = forms.CharField(max_length=30, error_messages={"required": "Confirm Password is required"},help_text="Confirm Password must be a strong password and match the new password")

    def clean(self):
        cd = super(ChangePassForm, self).clean()
        password = self.cleaned_data['password']

        current_password = self.cleaned_data['current_password']
        conf_password = self.cleaned_data['conf_password']

        # (?=.*[a-hj-np-z])(?=.*[A-HJ-NP-Z])(?=.*(\d|!0)).{8,}
        if len(password) < 8:
            self.add_error('password',
                           'Password must contains at least eight (8) alpha-numeric and special characters.')


        if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*[2-9])(?=.*(_|[^\w])).{8,}$', password):
            self.add_error('password', 'Password must contains alpha-numeric and special characters.')

        if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*[2-9])(?=.*(_|[^\w])).{8,}$', conf_password):
            self.add_error('password', 'Password must contains alpha-numeric and special characters.')

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

    def save(self, uid):

        cd = self.cleaned_data
        userdata = User.objects.get(id=uid)

        print("\n\n\n\n\n\nModule to change password for authenticated user\n\n{}\n\n\n\n\n\n".format(uid))

        if userdata.check_password(cd['current_password']):

            print("Valid Password: {}\n\n".format(cd['current_password']))

            userdata.set_password(cd['password'])
            userdata.save()

            return True

        else:
            self.add_error('current_password', 'Current Password must be your recent password.')


        return False


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

    def save(self):
#@w81mLBB01
        cd = self.cleaned_data
        #username = cd['email'].split("@")[0]
        print("\n\n\n\n\n\n\n\nSaving Data:\n{}\n\n\n\n\n\n\n\n\n\n".format(cd))

        userdata = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])

        userdata.first_name = cd['first_name']
        userdata.last_name = cd['last_name']
        userdata.is_staff = False

        userdata.is_active = True

        if userdata.save() :

            userprofile = UserProfile.objects.create(user_id=userdata.id, phone=cd['phone'], gender=cd['gender'], birthdate=cd['birthdate'])
            return userprofile.save()
       # print("\n\nData successfully save!\n\n")