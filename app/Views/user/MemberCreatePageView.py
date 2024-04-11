from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from ...tokens import account_activation_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from ...models import Company
from ...models import User
from django.conf import settings
from ... import forms
import random
import string
import json

class MemberCreatePageView(LoginRequiredMixin, View):
    template_name = 'user/member_create.html'
    form_class = forms.MemberForm

    def get(self, request):
        if request.htmx:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('members')

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)  

        if form.is_valid(): 
            user = form.save(commit=False)  

            account_id = request.user.account_id
            user.account_id = account_id
            
            if form.cleaned_data["email"]:
                user.username = form.cleaned_data["email"]
            else:
                user.username = "user"
            
            user.is_active = False
            user.save()
            print(user)

            self.joinMembersByEmail(request, user)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "memberListChanged": None,
                        "showMessage": f"{user.first_name} {user.last_name} a été ajouté.",
                    })
                }
            ) 
            
        else:
            return render(request, self.template_name, {'form': form})

    def joinMembersByEmail(self, request, user):
        mail_subject = "Rejoindre la Team"
        message = render_to_string(
            "user/join_members_by_email.html",
            {
                "user": user,
                "domain": get_current_site(request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                "protocol": "https" if request.scheme == "https" else "http",
            },
        )
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.content_subtype = "html"
        if email.send():
            messages.success(
                request,
                "Nous vous avons envoyé un lien de création de mot de passe à votre adresse e-mail. Vous devriez le recevoir sous peu.",
            )

        else:
            messages.error(
                request,
                "Problème d'envoi de l'e-mail de création du mot de passe, <b>PROBLÈME DE SERVEUR</b>",
            )

        return redirect(settings.LOGIN_URL)
