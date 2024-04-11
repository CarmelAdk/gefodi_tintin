from django.shortcuts import redirect,render
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views import View
from ... tokens import account_activation_token
from ... forms import ResetPasswordForm
from django.conf import settings
from django.contrib.auth import get_user_model


class ResetPasswordAccountPageView(View):
    template_name = 'authentication/reset_password.html'

    def get_user(self, uidb64):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=uid)
        except User.DoesNotExist:
            return None

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user and account_activation_token.check_token(user, token):
            form = ResetPasswordForm(user)
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, "Le lien est expiré !")
            return redirect(settings.LOGIN_URL)

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user and account_activation_token.check_token(user, token):
            form = ResetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Votre mot de passe a été changé avec succès. Vous pouvez continuer et <b>vous connecter </b>.")
                return redirect(settings.LOGIN_URL)
            
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
                return render(request, self.template_name, {'form': form})

        messages.error(request, "Le lien est expiréee !")
        return redirect(settings.LOGIN_URL)