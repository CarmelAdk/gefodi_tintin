from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=50,
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-icon-input",
                "id": "email",
                "placeholder": "nom@exemple.com",
                "pattern": r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
            }
        ),
    )
    password = forms.CharField(
        max_length=50,
        label="Mot de passe",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-icon-input",
                "id": "password",
                "placeholder": "Mot de passe",
            }
        ),
    )
    remember_me = forms.BooleanField(
        label="Rester connecté",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "id": "basic-checkbox"}
        ),
    )
