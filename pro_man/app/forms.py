from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput())
    password = forms.CharField(label='password',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['email','full_name','username','phone','role','password','password2']
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        
        allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
        domain = email.split('@')[-1]

        if domain not in allowed_domains:
            raise forms.ValidationError('Please use a valid email provider')

        return email
    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2 or len(password) < 8:
            raise forms.ValidationError('password does not match or len of it should be greater than 8')
        return cleaned_data
    