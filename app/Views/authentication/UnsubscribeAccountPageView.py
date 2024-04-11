from django.shortcuts import redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views import View
from ...tokens import account_activation_token
from django.conf import settings
from django.contrib.auth import get_user_model


class UnsubscribeAccountPageView(View):
    template_name = "authentication/activate_account.html"

    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None

        if user is not None and not user.is_active and not user.email_verified and account_activation_token.check_token(user, token):
            user.delete()
            messages.success(request, "Votre compte a été supprimé avec succès.")
        else:
            messages.error(request, "Le compte est déjà activé.")

        return redirect(settings.LOGIN_URL)