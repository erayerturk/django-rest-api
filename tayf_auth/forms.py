from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm as _PasswordResetForm, \
    SetPasswordForm as _SetPasswordForm
from django import forms

from tayf_auth.models import CustomUser


class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'input is-medium', 'placeholder': 'E-posta'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'input is-medium', 'placeholder': 'Parola'}
        )
    )


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'

        self.fields['email'].label = 'E-posta'
        self.fields['email'].widget.attrs['placeholder'] = 'E-posta'

        self.fields['first_name'].label = 'Ad'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ad'

        self.fields['last_name'].label = 'Soyad'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Soyad'

        self.fields['password1'].label = 'Parola'
        self.fields['password1'].widget.attrs['placeholder'] = 'Parola'

        self.fields['password2'].label = 'Tekrar Parola'
        self.fields['password2'].widget.attrs['placeholder'] = 'Parola Tekrar'

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class PasswordResetForm(_PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'input is-medium', 'placeholder': 'E-posta'})
    )


class SetPasswordForm(_SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'input is-medium', 'placeholder': 'Yeni Parola'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'input is-medium', 'placeholder': 'Yeni Parola (Tekrar)'}),
    )
