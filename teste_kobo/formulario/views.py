from datetime import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render

from django.utils.timezone import make_aware

from django.views.decorators.csrf import csrf_exempt

from formulario.models import Formulario
from teste_kobo import settings

# Create your views here.
def index(request):
    return render(request, "formulario/index.html")

@csrf_exempt
def webhook_kobo(request):

    token = settings.KOBO_WEBHOOK_TOKEN

    auth = request.headers.get("Authorization")

    print(token)
    print(auth)

    if auth != f"Bearer {token}":
                 
        return JsonResponse(
            {"erro": "Não autorizado"},
            status=401
        )

    if request.method != "POST":
        return JsonResponse(
             {"erro": "Método não permitido"},
            status=405
        )

    try:

            dados = json.loads(request.body)

            print(dados)

            kobo_id = dados.get("_id")
            uuid = dados.get("_uuid")
            data_envio=dados.get("_submission_time")

            if data_envio:
                data_envio = make_aware(
                    datetime.fromisoformat(data_envio)
                )

            nome = dados.get("Nome")
            idade = dados.get("Idade")
            hobbie = dados.get("hobbie")
            gosta_chocolate = True

            print("Aqui1")

            if dados.get("Gosta_de_Chocolate?") == "não":
                gosta_chocolate = False

            formulario, criado = Formulario.objects.update_or_create(
                kobo_id = kobo_id,

                defaults = {
                    "uuid":uuid,
                    "data_envio": data_envio,
                    "nome":nome,
                    "idade": int(idade),
                    "hobbie":hobbie,
                    "gosta_chocolate":gosta_chocolate
                }
            )

            print("Save")

            

            

            return JsonResponse(
                {"status": "sucesso"},
                status = 201
            )
            
    except Exception as erro:
        return JsonResponse(
            {"erro": str(erro)},
            status = 500
        )