from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
import re


class ResetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-2",
                "id": "new_password",
                "placeholder": "Nouveau mot de passe",
                "pattern": r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,}",
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=8,
                message="Le mot de passe doit avoir au moins 8 caractères.",
            ),
            RegexValidator(
                regex=re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,}"),
                message="Le mot de passe doit contenir au moins 8 caractères, au moins une lettre majuscule, une lettre minuscule, un chiffre, un caractère spécial (par exemple, @, #, $, etc.).",
            ),
        ],
    )
    new_password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-4",
                "id": "confirm_new_password",
                "placeholder": "Confirmer le nouveau mot de passe",
                "pattern": r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,}",
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=8,
                message="Le mot de passe doit avoir au moins 8 caractères.",
            ),
            RegexValidator(
                regex=re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,}"),
                message="Le mot de passe doit contenir au moins 8 caractères, au moins une lettre majuscule, une lettre minuscule, un chiffre, un caractère spécial (par exemple, @, #, $, etc.).",
            ),
        ],
    )

    class Meta:
        model = get_user_model()
        fields = []

    def __init__(self, user, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(user, *args, **kwargs)

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(
                "Les mots de passe ne correspondent pas. Veuillez les saisir à nouveau !"
            )
        return new_password2
