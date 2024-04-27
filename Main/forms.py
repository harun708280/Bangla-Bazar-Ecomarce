from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm

from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation
from .models import customers,Reviews
#Registration Form

class registrationform(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': "Enter your Email"}
        # labels = {'username': forms.Textarea(attrs={'class': 'form-control'})}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}
#LOGIN FORM
class loginform(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password=forms.CharField(label='Password',strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current_password','class':'form-control'}))

#PASSWORDCHNAGE FORM
    
class passwordchangeform(PasswordChangeForm):

    old_password=forms.CharField(label=_('Enter Old Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current_password','autofocus':True,'class':'form-control'}))

    new_password1=forms.CharField(label=_('Enter New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html)

    new_password2=forms.CharField(label=_('Confrim New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new password','class':'form-control'}))

class cprofile(forms.ModelForm):
    class Meta:
        model=customers
        fields=['first_name','last_name','Contract_Number','email','division','district','thana','Union']
        widgets={'first_name':forms.TextInput(attrs={'class':'form-control'}),'last_name':forms.TextInput(attrs={'class':'form-control'}),'Contract_Number':forms.NumberInput(attrs={'class':'form-control'}),'email':forms.TextInput(attrs={'class':'form-control'}),'division': forms.Select(attrs={'class':'form-control'}),'district':forms.TextInput(attrs={'class':'form-control'}),'thana':forms.TextInput(attrs={'class':'form-control'}),'Union':forms.TextInput(attrs={'class':'form-control'})}

class ReviewFrom(forms.ModelForm):
    class Meta:
        model=Reviews
        
        fields=('comment','rating')
        
class CuponcodeFrom(forms.Form):
    code=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))