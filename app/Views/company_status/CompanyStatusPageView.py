from django.shortcuts import render, redirect
from django.views.generic import View
from ... import forms
from ...models import CompanyStatus
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin

class CompanyStatusPageView(LoginRequiredMixin, View):
    template_name = 'company_status/company_status.html'
    form_class = forms.CompanyStatusForm

    def get(self, request):
        companies_status = CompanyStatus.objects.all().order_by('-id')
        form = self.form_class()
        return render(request, self.template_name, {'companies_status': companies_status, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid(): 
            company = form.save(commit=False)
            # Générer le slug à partir du statut de la société
            company.slug = slugify(company.status_name)
            company.save()
            return redirect('company_status')

        companies_status = CompanyStatus.objects.all().order_by('-id') 
        return render(request, self.template_name, {'companies_status': companies_status, 'form': form})