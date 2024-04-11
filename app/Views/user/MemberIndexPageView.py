from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
from django.core.paginator import Paginator
from ...models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class MemberIndexPageView(LoginRequiredMixin, View):
    template_name = 'user/index.html'
    
    # @login_required(login_url="login")
    def get(self, request):
        return render(request, self.template_name)