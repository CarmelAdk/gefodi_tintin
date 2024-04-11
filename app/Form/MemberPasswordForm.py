from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm

class MemberPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': "Les deux mots de passe ne correspondent pas.",
    }

    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirmation du mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.instance)
        return password2
