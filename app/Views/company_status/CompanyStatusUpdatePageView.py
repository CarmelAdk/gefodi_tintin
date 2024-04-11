from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.conf import settings
from ... import forms
from ...models import CompanyStatus
from django.contrib.auth.mixins import LoginRequiredMixin

class CompanyStatusUpdatePageView(LoginRequiredMixin, View):
    template_name = 'company_status/company_status_update.html'  
    form_class = forms.CompanyStatusForm

    def get(self, request, company_status_id, company_status_slug):
        company_status = get_object_or_404(CompanyStatus, id=company_status_id, slug=company_status_slug)
        form = self.form_class(instance=company_status)  
        return render(request, self.template_name, {'form': form, 'company_status': company_status})

    def post(self, request, company_status_id, company_status_slug):
        company_status = get_object_or_404(CompanyStatus, id=company_status_id, slug=company_status_slug)
        form = self.form_class(request.POST, request.FILES, instance=company_status)  

        if form.is_valid():
            updated_company_status = form.save(commit=False)
            # Récupérer le nouveau nom de l'entreprise après la modification
            new_company_status_slug = updated_company_status.slug
            form.save()  
            return redirect('company_status')

        return render(request, self.template_name, {'form': form, 'company_status': company_status})