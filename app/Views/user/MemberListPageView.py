from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
from django.core.paginator import Paginator
from ...models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class MemberListPageView(LoginRequiredMixin, View):
    template_name = 'user/members_list.html'

    def get(self, request):
        # Vérifie si l'utilisateur est connecté
        if request.user.is_authenticated:
            # Récupère l'account de l'utilisateur connecté
            user_account = request.user.account

            # Filtrer les membres associées à l'account de l'utilisateur connecté
            members = User.objects.filter(account=user_account).exclude(id=request.user.id).order_by('-id')
        else:
            # Si l'utilisateur n'est pas connecté, ne renvoie aucun membre
            members = []

        paginator = Paginator(members, settings.MEMBERS_PER_PAGE)  
        page_number = request.GET.get('page')  
        page_obj = paginator.get_page(page_number) 
        return render(request, self.template_name, {'members': page_obj})
