from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from ...models import Company
from django.contrib.auth.mixins import LoginRequiredMixin

class CompanyDeletePageView(LoginRequiredMixin, View):
    def get(self, request, company_id):
        # Récupérer l'entreprise à supprimer
        company = get_object_or_404(Company, pk=company_id)

        # Vérifier si l'utilisateur connecté est le propriétaire de l'entreprise
        if company.account_id == request.user.account_id:
            company.delete()

        return HttpResponseRedirect(reverse('company_list'))
