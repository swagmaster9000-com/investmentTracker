from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Profile
        fields = ['full_name', 'age', 'font', 'theme']

    def save(self, user):
        profile = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        user.save()
        profile.save()
