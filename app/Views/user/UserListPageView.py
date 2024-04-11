from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
from django.core.paginator import Paginator
from ...models import User

class UserListPageView(View):
    template_name = 'user/user_list.html'

    def get(self, request):
        users = User.objects.all().order_by('-id')
        paginator = Paginator(users, settings.COMPANIES_PER_PAGE)  # Paginer les entreprises en utilisant la constante définie dans le settings.py
        page_number = request.GET.get('page')  
        page_obj = paginator.get_page(page_number) 
        return render(request, self.template_name, {'users': page_obj})