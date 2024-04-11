from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.conf import settings
from ... import forms
from ...models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class MemberUpdatePageView(LoginRequiredMixin, View):
    template_name = 'user/member_update.html'  
    form_class = forms.MemberForm


    def get(self, request, member_id, member_last_name):
        member = get_object_or_404(User, id=member_id, last_name=member_last_name)

        # Vérifier si l'utilisateur connecté est le propriétaire du membre
        if member.account_id != request.user.account_id:
            # Si l'utilisateur n'est pas propriétaire du membre, rediriger vers une page d'erreur ou autre
            return redirect('error-404')  

        form = self.form_class(instance=member)  
        return render(request, self.template_name, {'form': form, 'member': member})

    # def post(self, request, member_id, member_last_name):
    #     member = get_object_or_404(User, id=member_id, last_name=member_last_name)
    #
    #     # Vérifier si l'utilisateur connecté est le propriétaire de l'entreprise
    #     if member.account_id != request.user.account_id:
    #         # Si l'utilisateur n'est pas propriétaire de l'entreprise, rediriger vers une page d'erreur
    #         return redirect('error-404')
    #
    #     form = self.form_class(request.POST, request.FILES, instance=member)
    #
    #     if form.is_valid():
    #         updated_member = form.save(commit=False)
    #         # Récupérer le nouveau nom du membre après la modification
    #         new_member_last_name = updated_member.last_name
    #         form.save()
    #         return redirect('members_list')
    #
    #     return render(request, self.template_name, {'form': form, 'member': member})



    #
    # def post(self, request, member_id, member_last_name):
    #     member = get_object_or_404(User, id=member_id, last_name=member_last_name)
    #
    #     # Vérifier si l'utilisateur connecté est le propriétaire de l'entreprise
    #     if member.account_id != request.user.account_id:
    #         # Si l'utilisateur n'est pas propriétaire de l'entreprise, rediriger vers une page d'erreur
    #         return redirect('error-404')
    #
    #     form = self.form_class(request.POST, request.FILES, instance=member)
    #
    #     if form.is_valid():
    #         updated_member = form.save(commit=False)
    #         # Récupérer le nouveau nom du membre après la modification
    #         new_member_last_name = updated_member.last_name
    #         form.save()
    #         return redirect('members_list')
    #
    #     return render(request, self.template_name, {'form': form, 'member': member})
