from django import forms
from .models import Product
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields=["name","description","price","file"]


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username' , 'email','first_name','password1','password2']

    def check_password(self):
        if self.cleaned_data['password']!=self.cleaned_data['password2']:
            raise forms.ValidationError('password fields not match')
        return self.cleaned_data['password2']