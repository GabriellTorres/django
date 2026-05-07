from django.http import HttpResponse

def index_view(request):
    return HttpResponse("<h1>Bem-vindo!</h1>")

def teste_view(request):
    return HttpResponse("Hello World")