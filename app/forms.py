from django import forms
from django.contrib.auth.forms import UsernameField,UserChangeForm,UserCreationForm,AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext,gettext_lazy as _

from .models import Customer,cart

class CustomerRegistrationForm(UserCreationForm):
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label="Password Confirm(again)",widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=["username","email"]
        labels={"email":"Email"}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'}),'email':forms.EmailInput(attrs={'class':'form-control'})}


class UserLoginForm(AuthenticationForm):
    #username=forms.CharField(widget=forms.TextInput(attrs={'class':"form-control","autofocus":True}))
    username=UsernameField(widget=forms.TextInput(attrs={'class':"form-control","autofocus":True}))
    
    password=forms.CharField(label="Password",strip=False,widget=forms.PasswordInput(attrs={'class':"form-control","autocomplete":"current-password"}))



class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label="Old Password",strip=False,
    widget=forms.PasswordInput(attrs={'class':'form-control',
    'autocomplete':'current-password','autofocus':True}))
    
    new_password1=forms.CharField(label="New Password",strip=False,
    widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'new-password'}),
    help_text=password_validation.password_validators_help_text_html())

    new_password2=forms.CharField(label="Confirm Password",strip=False,
    widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'new-password'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email",'class':'form-control'}),
    )

class MyPasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class":"form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class":'form-control'}),
    )


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=["name","address","city","state","zipcode"]
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'})
        }


class EditUserProfileForm(UserChangeForm):
    password=None
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=["username","first_name","last_name","email"]
        widgets={
            "username":forms.TextInput(attrs={'class':'form-control'}),
            "first_name":forms.TextInput(attrs={'class':'form-control'}),
            "last_name":forms.TextInput(attrs={'class':'form-control',"requred":'required'}),
            "email":forms.TextInput(attrs={'class':'form-control',"requred":'required'}),
        }


class CustomerAddresUpdateForm(forms.ModelForm):
    # user=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'disabled':'disabled'}))
    contact_no=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model=Customer
        fields="__all__"
        exclude=["user"]
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
        }
        
    # def __init__(self,*args,**kwargs):
    #     super(CustomerAddresUpdateForm,self).__init__(*args,**kwargs)
    #     self.fields["user"].widget.attrs['disabled']=True
