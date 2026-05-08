from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Comments, Post, Profile, Category, Report

# Add comments
class CommentForm(forms.ModelForm):
    class Meta():
        model = Comments
        fields = ['body']

INPUT_CLASS = 'w-full border-none outline-none py-2 font-light text-xs bg-transparent text-black placeholder-gray-300 hover:placeholder-gray-500 transition-all duration-300'

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': INPUT_CLASS,
        'placeholder': 'Enter your email',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': INPUT_CLASS,
            'placeholder': 'Enter your username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': INPUT_CLASS,
            'placeholder': 'Enter your password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': INPUT_CLASS,
            'placeholder': 'Confirm your password',
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full border-none outline-none py-3 font-light text-sm bg-transparent text-black placeholder-gray-300 hover:placeholder-gray-500 transition-all duration-300',
        'placeholder': 'Enter your username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full border-none outline-none py-3 font-light text-sm bg-transparent text-black placeholder-gray-300 hover:placeholder-gray-500 transition-all duration-300',
        'placeholder': 'Enter your password',
    }))

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            profile.save()
        return profile


# Report update
class ReportForm(forms.ModelForm):
        class Meta:
            model = Report
            fields = ['reason','details']
            widgets = {
                'reason': forms.Select(attrs = {
                    'class': INPUT_CLASS,
                }),
                'details': forms.Textarea(attrs = {
                    'class': INPUT_CLASS,
                    'placeholder': 'Additional details (optional)',
                    'rows': 1,
                }),
            }
