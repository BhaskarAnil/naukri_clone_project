from django import forms
from .models import User, Company, Profile
from django.contrib.auth import authenticate

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    mobile = forms.CharField(max_length=10)
    is_employer = forms.BooleanField(required=False)
    company_name = forms.CharField(max_length=255, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose a different one.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists. Please use another email or login.')
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError('Please enter a valid 10-digit mobile number.')
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        is_employer = cleaned_data.get('is_employer', False)
        company_name = cleaned_data.get('company_name', '').strip() if is_employer else ''
        if is_employer and not company_name:
            self.add_error('company_name', 'Company name is required for employers.')
        return cleaned_data

    def save(self):
        is_employer = self.cleaned_data.get('is_employer', False)
        company_name = self.cleaned_data.get('company_name', '').strip() if is_employer else ''
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            is_employer=is_employer,
            mobile=self.cleaned_data['mobile']
        )
        if is_employer and company_name:
            company = Company.objects.filter(user=user).first()
            if company:
                company.company_name = company_name
                company.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('No user found with these credentials. Please check your username and password and try again.')
        cleaned_data['user'] = user
        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'location', 'experience', 'skills', 'resume_url']
        widgets = {
            'experience': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'resume_url': forms.URLInput(attrs={'placeholder': 'Paste your Google Drive link here'})
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_logo_url', 'description']
        widgets = {
            'company_logo_url': forms.URLInput(attrs={'placeholder': 'Paste your Google Drive image link here'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
