from django import forms

class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control flex-1",
                "id": "email",
                "placeholder": "nom@exemple.com",
                "pattern": r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
            }
        ),
    )