from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import View

class SignOutPageView(View):
    template_name = 'authentication/signout.html'
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home')
        logout(request)
        # return redirect('template_name')
        return render(request, self.template_name)
