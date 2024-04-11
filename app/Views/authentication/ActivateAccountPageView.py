from django.shortcuts import redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views import View
from ...tokens import account_activation_token
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from app.Entity import Account


class ActivateAccountPageView(View):
    template_name = "authentication/activate_account.html"

    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            expiration_time = user.date_joined + timedelta(hours=24)
            if timezone.now() <= expiration_time:
                user.is_active = True
                user.email_verified = True
                user.save()

                messages.success(
                    request,
                    "Merci pour la confirmation de votre email. Vous pouvez maintenant vous connecter à votre compte.",
                )
            else:
                account_id = user.account_id
                user.delete()

                if account_id:
                    Account.objects.filter(pk=account_id).delete()
                    
                messages.error(request, "Le lien d'activation a expiré. Veuillez vous réinscrire!")
        else:
            messages.error(request, "Le lien d'activation n'est pas valide!")

        return redirect(settings.LOGIN_URL)
