from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from django.views.generic import View
from django.conf import settings
from ... import forms
from ... tokens import account_activation_token

import requests


class ForgotPasswordPageView(View):

    template_name = "authentication/forgot_password.html"
    form_class = forms.ForgotPasswordForm

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

                email = form.cleaned_data["email"]
                associated_user = get_user_model().objects.filter(Q(email=email)).first()

                if associated_user:
                    subject = "Demande de réinitialisation du mot de passe"
                    message = render_to_string(
                        "authentication/reset_account_password.html",
                        {
                            "user": associated_user,
                            "domain": get_current_site(request).domain,
                            "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                            "token": account_activation_token.make_token(associated_user),
                            "protocol": "https" if request.is_secure() else "http",
                        },
                    )
                    email = EmailMessage(subject, message, to=[associated_user.email])
                    email.content_subtype = "html"
                    if email.send():
                        messages.success(
                            request,
                            "Nous vous avons envoyé un lien de réinitialisation de mot de passe à votre adresse e-mail, si un compte existe avec l'e-mail que vous avez saisi. Vous devriez le recevoir sous peu. Si vous ne recevez pas d'e-mail, assurez-vous d'avoir saisi l'adresse avec laquelle vous vous êtes inscrit et vérifiez votre dossier spam.",
                        )

                    else:
                        messages.error(
                            request,
                            "Problème d'envoi de l'e-mail de réinitialisation du mot de passe, <b>PROBLÈME DE SERVEUR</b>",
                        )

                    return redirect(settings.LOGIN_URL)
                
                else:
                    messages.success(
                            request,
                            "Nous vous avons envoyé un lien de réinitialisation de mot de passe à votre adresse e-mail, si un compte existe avec l'e-mail que vous avez saisi. Vous devriez le recevoir sous peu. Si vous ne recevez pas d'e-mail, assurez-vous d'avoir saisi l'adresse avec laquelle vous vous êtes inscrit et vérifiez votre dossier spam.",
                        )
                    return redirect(settings.LOGIN_URL)
                
            else:
                messages.error(request, "Validation reCAPTCHA échouée. Veuillez réessayer.")
                return render(request, self.template_name, {"form": form})

        return render(request, self.template_name, {"form": form})
