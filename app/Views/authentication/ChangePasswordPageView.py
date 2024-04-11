from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.conf import settings
from ... import forms
from django.contrib.auth import update_session_auth_hash


class ChangePasswordPageView(View):

    template_name = 'authentication/reset_password.html'
    form_class = forms.ResetPasswordForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']


            if new_password != confirm_new_password:
                messages.error(request, 'Les nouveaux mots de passe ne correspondent pasaaaaa.')
                return render(request, self.template_name, {'form': form})

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            # messages.success(request,'Votre mot de passe a été changé avec succès.')
            return redirect(settings.LOGIN_URL)

        return render(request, self.template_name, {'form': form})
