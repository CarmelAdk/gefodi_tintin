from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.conf import settings
from ... import forms
from ...models import Company
from django.contrib.auth.mixins import LoginRequiredMixin

class CompanyUpdatePageView(LoginRequiredMixin, View):
    template_name = 'company/company_update.html'  
    form_class = forms.CompanyForm

    def get(self, request, company_id, company_slug):
        company = get_object_or_404(Company, id=company_id, slug=company_slug)

        # Vérifier si l'utilisateur connecté est le propriétaire de l'entreprise
        if company.account_id != request.user.account_id:
            # Si l'utilisateur n'est pas propriétaire de l'entreprise, rediriger vers une page d'erreur ou autre
            return redirect('error-404')  

        form = self.form_class(instance=company)  
        return render(request, self.template_name, {'form': form, 'company': company})

    def post(self, request, company_id, company_slug):
        company = get_object_or_404(Company, id=company_id, slug=company_slug)

        # Vérifier si l'utilisateur connecté est le propriétaire de l'entreprise
        if company.account_id != request.user.account_id:
            # Si l'utilisateur n'est pas propriétaire de l'entreprise, rediriger vers une page d'erreur 
            return redirect('error-404')  

        form = self.form_class(request.POST, request.FILES, instance=company)  

        if form.is_valid():
            updated_company = form.save(commit=False)
            # Récupérer le nouveau nom de l'entreprise après la modification
            new_company_slug = updated_company.slug
            form.save()  
            return redirect('company_detail', company_id=company_id, company_slug=new_company_slug)

        return render(request, self.template_name, {'form': form, 'company': company})
