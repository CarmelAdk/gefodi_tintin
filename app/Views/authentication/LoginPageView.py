from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.views.generic import View
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from ... import forms
import requests


class LoginPageView(View):

    template_name = "authentication/login.html"
    form_class = forms.LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        form = self.form_class()
        recaptcha_public_key = settings.RECAPTCHA_PUBLIC_KEY
        return render(
            request, self.template_name, context={"form": form, "recaptcha_public_key": recaptcha_public_key}
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            recaptcha_secret_key = settings.RECAPTCHA_PRIVATE_KEY
            data = {
                'secret': recaptcha_secret_key,
                'response': recaptcha_response
            }
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            
            if result['success']:
                user = authenticate(
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                )
                if user is not None and user.is_active is True:
                    login(request, user)

                    if form.cleaned_data.get("remember_me"):
                        request.session.set_expiry(timezone.now() + timedelta(weeks=1))
                    else:
                        request.session.set_expiry(0)

                    return redirect("home")
            else:
                messages.error(request, "Validation reCAPTCHA échouée. Veuillez réessayer.")
                return render(request, self.template_name, {"form": form})

        messages.error(request, "Identifiants invalides. Veuillez vérifier votre email et votre mot de passe.")
        return render(
            request, self.template_name, context={"form": form}
        )
