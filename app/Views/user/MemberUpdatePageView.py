from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ...models import User
import json
from django.shortcuts import render, redirect, get_object_or_404
from ... import forms



class MemberUpdatePageView(View):
    template_name = 'user/member_update.html'
    form_class = forms.MemberForm

    @csrf_exempt
    @require_http_methods(["POST"])  # Assurez-vous que la vue accepte uniquement les requêtes POST
    def update_data(request):
        try:
            # Extraction des données envoyées par AJAX
            data = json.loads(request.body)
            objet_id = data.get('id_user')
            lastname = data.get(
                'last_name')  # Assurez-vous que ces clés correspondent à celles envoyées par AJAX

            # Mise à jour de l'objet
            objet = User.objects.get(id=objet_id)
            objet.last_name = lastname  # Assurez-vous que 'champ' est un champ valide de votre modèle
            objet.save()

            # Réponse indiquant le succès de l'opération
            return JsonResponse({"success": True, "message": "Données mises à jour avec succès."})

        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "Objet non trouvé."}, status=404)
        except Exception as e:
            # Réponse en cas d'erreur
            return JsonResponse({"success": False, "message": str(e)}, status=400)


    def get(self, request, member_id):
        if request.htmx:
            user = get_object_or_404(User, pk=member_id)
            form = self.form_class(instance=user)
            return render(request, self.template_name, {'form': form, 'member' : user})
        else:
            return redirect('members')


    def post(self, request, member_id):
        user = get_object_or_404(User, pk=member_id)
        form = self.form_class(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "memberListChanged": None,
                        "showMessage": f"{user.first_name} {user.last_name} a été mis à jour.",
                    })
                }
            )            

        else:
            return render(request, self.template_name, {'form': form, 'member' : user})
