from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
from django.core.paginator import Paginator
from ...models import Company
from django.contrib.auth.mixins import LoginRequiredMixin

class CompanyListPageView(LoginRequiredMixin, View):
    template_name = 'company/company_list.html'

    def get(self, request):
        # Vérifie si l'utilisateur est connecté
        if request.user.is_authenticated:
            # Récupère l'account de l'utilisateur connecté
            user_account = request.user.account

            # Filtrer les entreprises associées à l'account de l'utilisateur connecté
            companies = Company.objects.filter(account=user_account).order_by('-id')
        else:
            # Si l'utilisateur n'est pas connecté, ne renvoie aucune entreprise
            companies = []

        paginator = Paginator(companies, settings.COMPANIES_PER_PAGE)  
        page_number = request.GET.get('page')  
        page_obj = paginator.get_page(page_number) 
        return render(request, self.template_name, {'companies': page_obj})
