from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from ...models import Company
from django.contrib.auth.mixins import LoginRequiredMixin

class CompanyDetailPageView(LoginRequiredMixin, View):
    template_name = 'company/company_detail.html'

    def get(self, request, company_id, company_slug):
        # Récupérer l'entreprise
        company = get_object_or_404(Company, id=company_id, slug=company_slug)

        # Vérifier si l'utilisateur connecté est le propriétaire de l'entreprise
        if company.account_id != request.user.account_id:
            # Si l'utilisateur n'est pas propriétaire de l'entreprise, rediriger vers une page d'erreur 
            return redirect('error-404') 

        return render(request, self.template_name, {'company': company})
