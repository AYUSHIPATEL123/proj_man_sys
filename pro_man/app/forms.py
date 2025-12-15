from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput())
    password = forms.CharField(label='password',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['email','full_name','username','phone','role','password','password2']

        def validate(self):
            if not self.cleaned_data['email'].endswith('@gmil.com'):
                raise forms.ValidationError('email must end with @gmil.com')
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError('password not matched')
            if len(self.cleaned_data['password']) < 8:
                return forms.ValidationError('password must be at least 8 characters')
            return self.cleaned_data
        
class LoginForm(AuthenticationForm):
    # email = forms.CharField(label='email',widget=forms.EmailInput())
    password = forms.CharField(label='password',widget=forms.PasswordInput()) 
