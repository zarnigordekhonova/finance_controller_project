from django import forms
from Users.models import CustomUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


phone_number_regex = RegexValidator(
    regex=r'^\+?(\d{1,3})?\d{9,25}$',
    message="Phone number must be entered in the format: '+998 00 000-00-00'. Up to 25 digits allowed."
)


class CustomUserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        min_length=8,
        label='Password',
        widget=forms.PasswordInput,
        help_text="Password should be at least 8 characters long."
    )
    password2 = forms.CharField(
        min_length=8,
        label='Password confirm',
        widget=forms.PasswordInput,
        help_text='Enter the same password as before, for verification.'
    )
    phone_number = forms.CharField(
        validators=[phone_number_regex],
        max_length=15,
        help_text="Phone number must be entered in the format: '+998 00 000-00-00'. Up to 25 digits allowed."
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            return user

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise ValidationError('Passwords do not match')
        return cd['password2']


class ProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(
        min_length=8,
        label='Password',
        widget=forms.PasswordInput,
        help_text="Password should be at least 8 characters long.",
    )

    password2 = forms.CharField(
        min_length=8,
        label='Password confirm',
        widget=forms.PasswordInput,
        help_text='Enter the same password as before, for verification.',
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'image']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            return user

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise ValidationError('Passwords do not match')
        return cd['password2']
