from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView

from ...forms import MemberPasswordForm

User = get_user_model()

class MemberPasswordPageView(FormView):
    template_name = 'user/member_password_form.html'
    form_class = MemberPasswordForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        # Récupérer l'utilisateur correspondant à l'UIDB64 et au token
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None

        # Vérifier que le token est valide pour cet utilisateur
        if self.user is not None and default_token_generator.check_token(self.user, token):
            return super().dispatch(request, *args, **kwargs)
        else:
            # Si le token n'est pas valide, rediriger vers une page d'erreur appropriée
            return render(request, 'error_page.html')

    def form_valid(self, form):
        # Définir le nouveau mot de passe pour l'utilisateur
        form.save()
        return redirect(self.success_url)
