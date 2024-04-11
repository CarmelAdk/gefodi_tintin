from django.shortcuts import render, redirect
from django.views.generic import View
from ... import forms
from ...models import Company
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin

class CompanyCreatePageView(LoginRequiredMixin, View):
    template_name = 'company/company_create.html'
    form_class = forms.CompanyForm

    def get(self, request):
        form = self.form_class()  # Créer une instance vide du formulaire
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)  # Crée une instance du formulaire avec les données soumises

        if form.is_valid(): 
            company = form.save(commit=False)  
            
            # Récupérer l'ID du compte de l'utilisateur connecté
            account_id = request.user.account_id

            # Associer l'ID du compte de l'utilisateur à l'entreprise
            company.account_id = account_id

            # Générer le slug à partir du nom de la société
            company.slug = slugify(company.name)

            company.save()
            return redirect('company_list')

        # Si le formulaire n'est pas valide, rend à nouveau le template avec le formulaire et les erreurs
        return render(request, self.template_name, {'form': form})