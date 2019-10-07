from django import forms

class MerchantForm(forms.Form):

    last_name = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    email = forms.CharField(max_length=254)

    company_name = forms.CharField(max_length=100)
    contact_name = forms.CharField(max_length=100)
    contact_title = forms.CharField(max_length=100)
    phone = forms.RegexField(regex="^(\+63|0)9[0-9]{9}$" ,max_length=13)

    telephone = forms.CharField(max_length=100)
    fax = forms.CharField(max_length=100)
    company_logo = forms. CharField(max_length=100)
    payment_methods = forms.MultipleChoiceField()
