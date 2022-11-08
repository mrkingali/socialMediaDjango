from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class UserRegistrationForm(forms.Form):


    username=forms.CharField(widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'your user name'}))
    emailAdress=forms.EmailField(widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'youremail@email.com'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={ 'class':'form-control','placeholder':'your pass'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={ 'class':'form-control','placeholder':'confirm your pass'}))
    firstname=forms.CharField(widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'your firstname'}),required=False)
    lastname=forms.CharField(widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'your lastname'}),required=False)

    def clean_emailAdress(self):
        email=self.cleaned_data['emailAdress']
        exists=User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError("this emailAdress exist")
        return email

    def clean_username(self):
        username=self.cleaned_data['username']
        exists=User.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("this user name already taken")
        return username

    def clean(self):
        cleaned_data=super().clean()
        p1=cleaned_data.get('password')
        p2=cleaned_data.get('password2')
        if p1 and p2 and p1!=p2:
            raise ValidationError("passwords must match")

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your user name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'passwor'}))





