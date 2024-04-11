from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import User
from django.views.generic import View

class HomePageView(LoginRequiredMixin, View):
    template_name = 'homepage/home.html'

    def get(self, request):
        users = User.objects.all()
        return render(request, self.template_name, {'users': users})
