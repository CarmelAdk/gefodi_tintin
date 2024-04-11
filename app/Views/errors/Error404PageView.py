from django.shortcuts import render
from django.views import View  

class Error404PageView(View):
    template_name = 'errors/error_404.html'

    def get(self, request, exception=None): 
        return render(request, self.template_name)
