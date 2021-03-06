from django import forms

from django.contrib.auth.models import User

from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives

from django.template.loader import get_template, render_to_string

from django.shortcuts import get_object_or_404

from django.contrib.auth import update_session_auth_hash

from .models import UserProfile, Address
from datetime import date, timedelta, datetime

import re   # Regular Expression
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('C', 'Custom'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing Address'),
    ('S', 'Shipping Address'),
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




class UserProfileForm(forms.Form):

    phone = forms.RegexField(regex=r"^(\+63|0)9[0-9]{9}$", max_length=13, error_messages={"invalid":"Phone number is invalid format","required": "Mobile Phone is required."})
    gender = forms.ChoiceField(choices=GENDER)
    birthdate = forms.DateField(input_formats=['%Y/%m/%d'])
    password = forms.CharField(max_length=30, error_messages={"required": "Password is required"}, help_text="New Password must be a strong password")

    def clean(self):

        cd = super(UserProfileForm, self).clean()
        password = self.cleaned_data['password']

        # (?=.*[a-hj-np-z])(?=.*[A-HJ-NP-Z])(?=.*(\d|!0)).{8,}
        if len(password) < 8:
            self.add_error('password',
                           'Password must contains at least eight (8) alpha-numeric and special characters.')

        if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*[2-9])(?=.*(_|[^\w])).{8,}$', password):
            self.add_error('password', 'Password must contains alpha-numeric and special characters.')



        return cd

    def clean_birthdate(self):
        today = date.today()
        cd = self.cleaned_data

        #bday = datetime.strptime(cd['birthdate'], "%m-%d-%Y").date()

        print("\n\n\n\n\nBirthdate Format : {}\n\n\n\n".format(cd['birthdate']))

        age = (today - cd['birthdate']) // timedelta(days=365.2425)

        if age < 18:
            raise forms.ValidationError('Age must be atleast 18yrs old.')

        return cd['birthdate']

    def save(self, uid):

        cd = self.cleaned_data

        userdata = User.objects.get(id=uid)

        if userdata.check_password(cd['password']):
            u = UserProfile.objects.get(user_id=uid)

            u.phone = cd['phone']
            u.gender = cd['gender']
            u.birthdate = cd['birthdate']

            u.save()

            return True

        else:
            self.add_error('password', 'Password must be your recent password.')


        return False



class UserRegistrationForm(forms.Form):

    email = forms.EmailField(max_length=254, error_messages={"required": "Email is required."})
    username = forms.CharField(max_length=64, error_messages={"required":"Username is required."})
    first_name = forms.RegexField(regex="^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$", max_length=64, error_messages={"required": "First name is required."})
    last_name = forms.RegexField(regex="^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$", max_length=64, error_messages={"required":"Last name is required"})
    password = forms.CharField(max_length=30, error_messages={"required":"Password is required"}, help_text="Password must be a strong password")
    conf_password = forms.CharField(max_length=30, error_messages={"required":"Confirm Password is required."})
    phone = forms.RegexField(regex=r"^(\+63|0)9[0-9]{9}$", max_length=13, error_messages={"invalid":"Phone number is invalid format","required": "Mobile Phone is required."})
    gender = forms.ChoiceField(choices=GENDER)
    birthdate = forms.DateField(input_formats=['%Y-%m-%d'])

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
    
    def clean_birthdate(self):
        today = date.today()
        cd = self.cleaned_data

        #bday = datetime.strptime(cd['birthdate'], "%m-%d-%Y").date()

        #print("\n\n\n\n\nBirthdate Format : {}\n\n\n\n".format(cd['birthdate']))

        age = (today - cd['birthdate']) // timedelta(days=365.2425)

        if age < 18:
            self.add_error('birthdate', 'Birthdate must be atleast 18yrs old.')

        return cd['birthdate']
    
    def save(self):
#@w81mLBB01
        cd = self.cleaned_data
        #username = cd['email'].split("@")[0]

        userdata = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])



        userdata.first_name = cd['first_name']
        userdata.last_name = cd['last_name']
        userdata.is_staff = False

        userdata.is_active = True

        userprofile = UserProfile.objects.create(user_id=userdata.id, phone=cd['phone'], gender=cd['gender'], birthdate=cd['birthdate'])


        return userprofile.save()


class UserAddressForm(forms.Form):

    consignee = forms.CharField(max_length=100, error_messages={"required": "First name is required."})

    phone_number = forms.RegexField(regex=r"^(\+63|0)9[0-9]{9}$", max_length=13, error_messages={"invalid": "Phone number is invalid format", "required": "Mobile Phone is required."})

    landmark = forms.CharField(max_length=100)
    detailed_address = forms.CharField(max_length=100)
    barangay = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    province = forms.CharField(max_length=100)
    region = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=4)

    address_type = forms.ChoiceField(choices=ADDRESS_CHOICES)
    default_status = forms.BooleanField(required=False)
    password = forms.CharField(max_length=30, error_messages={"required": "Password is required"}, help_text="Password must be a strong password")

    def clean(self):

        cd = super(UserAddressForm, self).clean()

        print("\n\n\n\n\n\n\nBefore Cleaning UserAddressForm\n\n{}\n\n".format(cd))
        password = cd['password']
        if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*[2-9])(?=.*(_|[^\w])).{8,}$', password):
            self.add_error('password', 'Password must contains alpha-numeric and special characters.')

        if len(password) < 8:
            self.add_error('password', 'Password must contains at least eight (8) alpha-numeric and special characters.')

        print("\n\n\n\n\n\n\nAfter Cleaning UserAddressForm\n\n{}\n\n".format(cd))

        return cd


    def clean_zip_code(self):

        cd = self.cleaned_data

        zip_code = cd['zip_code']

        if not re.match('^[0-9]{4}$', zip_code):
            self.add_error('zip_code', 'Zip Code must contains 4 numeric characters.')

        return zip_code

    def clean_city(self):

        cd = self.cleaned_data

        city = cd['city']

        if not re.match("^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$", city):
            self.add_error('city', 'City name must be contain alpha characters and space.')

        return city

    def save(self, user_id):
        print("\n\n\n\n\nSaving UserAddressForm\n\n\n\n\n\n")
        cd = self.cleaned_data

        uauth = User.objects.get(id=user_id)
        if uauth.check_password(cd['password']):

            new_address = Address.objects.create(consignee=cd['consignee'], phone_number=cd['phone_number'],region = cd['region'],
                                                 user_id=user_id, landmark = cd['landmark'],province = cd['province'],
                                                 detailed_address = cd['detailed_address'], barangay = cd['barangay'], city = cd['city'],
                                                 zip_code = cd['zip_code'], address_type = cd['address_type'], default = cd['default_status'])

            new_address.save()

            last_id = new_address.id

            address_list = Address.objects.get(user_id=user_id)

            if cd['default_status']:

                # Updating tables

                for address in address_list:
                    if not address.id == last_id:
                        address.default = False

            return True
        else:
            self.add_error('password', 'Password must be your recent password.')

        return False