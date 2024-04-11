from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from ...models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class MemberDeletePageView(LoginRequiredMixin, View):
    def get(self, request, member_id):
        # Récupérer l'entreprise à supprimer
        member = get_object_or_404(User, pk=member_id)

        # Vérifier si l'utilisateur connecté est le propriétaire de l'entreprise
        if member.account_id == request.user.account_id:
            member.delete()

        return HttpResponseRedirect(reverse('members'))
