from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from ...models import CompanyStatus
from django.contrib.auth.mixins import LoginRequiredMixin

class CompanyStatusDeletePageView(LoginRequiredMixin, View):
    def get(self, request, company_status_id):
        company = get_object_or_404(CompanyStatus, pk=company_status_id)
        company.delete()
        return HttpResponseRedirect(reverse('company_status'))