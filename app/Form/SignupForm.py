from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from app.Entity import Role, Account
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
import re


class SignupForm(UserCreationForm):
    # username = forms.CharField(
    #     min_length=3,
    #     max_length=19,
    #     label="Nom d'utilisateur",
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "id": "username",
    #             "placeholder": "Nom d'utilisateur",
    #             "pattern": r"[a-zA-Z][a-zA-Z0-9\-_]{2,49}",
    #         }
    #     ),
    # )
    last_name = forms.CharField(
        min_length=2,
        max_length=19,
        label="Nom",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "last_name",
                "placeholder": "Nom",
                "pattern": r"([a-zA-ZÀ-ÖØ-öø-ÿ][a-zA-ZÀ-ÖØ-öø-ÿ\-' ]{1,18})",
                
            }
        ),
    )
    first_name = forms.CharField(
        min_length=2,
        max_length=19,
        label="Prénom",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "first_name",
                "placeholder": "Prénom",
                "pattern": r"([a-zA-ZÀ-ÖØ-öø-ÿ][a-zA-ZÀ-ÖØ-öø-ÿ\-' ]{1,18})",
            }
        ),
    )
    email = forms.EmailField(
        max_length=50,
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "email",
                "placeholder": "nom@exemple.com",
                "pattern": r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,4}",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=50,
        label="Mot de passe",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-icon-input",
                "id": "password",
                "placeholder": "Mot de passe",
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
    password2 = forms.CharField(
        max_length=50,
        label="Confirmer",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-icon-input",
                "id": "confirmPassword",
                "placeholder": "Confirmer le mot de passe",
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
    cgu_rgpd = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "id": "termsService"}
        ),
    )

    class Meta:
        model = get_user_model()
        fields = (
            # "username",
            "last_name",
            "first_name",
            "email",
            "password1",
            "password2",
            "cgu_rgpd",
        )

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     if get_user_model().objects.filter(username=username).exists():
    #         raise forms.ValidationError(
    #             "Ce nom d'utilisateur est déjà utilisé. Veuillez en choisir un autre."
    #         )
    #     return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Cette adresse e-mail est déjà associée à un compte. Veuillez utiliser une autre adresse e-mail."
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Les mots de passe ne correspondent pas. Veuillez les saisir à nouveau."
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        manager_role = Role.objects.get(name="MANAGER")
        user.role = manager_role
        user.cgu_rgpd = self.cleaned_data["cgu_rgpd"]
        

        account = Account.objects.create()
        account.user_subscriber = account.generate_unique_subscriber_number()
        account.is_active = True

        user.account_id = account.id

        if commit:
            user.save()

        return user
