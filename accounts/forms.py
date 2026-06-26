#ACCOUNTS FORMS
from django import forms
from accounts.models import C_User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import C_User

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = C_User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if C_User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email already exists. Please try another email."
            )
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())


class EditEmailForm(forms.ModelForm):
    class Meta:
        model= C_User
        fields=['email']

        widgets={
            'email':forms.EmailInput(attrs={'class':'form-control'})
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance
        if user.email == email:
            return email
        if C_User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("This email is already registered to another account.")            
        return email
  
class C_PasswordResetForm(forms.Form):
    new_password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        label='New Password'
    )
    confirm_password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_pass = cleaned_data.get('new_password')
        confirm_pass = cleaned_data.get('confirm_password')
        
        if new_pass and confirm_pass and new_pass != confirm_pass:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data


