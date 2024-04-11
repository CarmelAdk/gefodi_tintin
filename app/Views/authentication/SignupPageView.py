from django.shortcuts import render, redirect
from django.contrib import messages

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from django.views.generic import View
from django.conf import settings
from ... import forms
from ...tokens import account_activation_token
import requests


class SignupPageView(View):

    template_name = "authentication/signup.html"
    form_class = forms.SignupForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        form = self.form_class()
        recaptcha_public_key = settings.RECAPTCHA_PUBLIC_KEY
        return render(request, self.template_name, context={"form": form, "recaptcha_public_key": recaptcha_public_key})

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
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                self.activateEmail(request, user, form.cleaned_data.get("email"))
                return redirect(settings.LOGIN_URL)
            else:
                messages.error(request, "Validation reCAPTCHA échouée. Veuillez réessayer.")
                return render(request, self.template_name, context={"form": form})

        return render(request, self.template_name, context={"form": form})

    def activateEmail(self, request, user, to_email):
        mail_subject = "Activez votre compte utilisateur"
        message = render_to_string(
            "authentication/activate_account.html",
            {
                "user": user,
                "domain": get_current_site(request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                "protocol": "https" if request.is_secure() else "http",
            },
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        if email.send():

            messages.success(
                request,
                f"Chèr(e) <b>{user}</b>, veuillez accéder à votre e-mail <b>{to_email}</b> et vous rendre dans votre boîte de réception et cliquer sur lien d'activation pour confirmer et terminer votre inscription. <b>Remarque:</b> Vérifiez vos spams.",
            )

        else:
            messages.error(
                request,
                f"Problème de l'envoi du mail à  {to_email}; verifiez si vous avez bien saissie votre mail",
            )
