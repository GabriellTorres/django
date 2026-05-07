from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from tarefas.forms import TarefaForm
from tarefas.models import TarefaModel

# Create your views here.

def tarefas_home(request):
    contexto = {
        "nome":"Fulano",
        "tarefas":TarefaModel.objects.all()
    }
    return render(request, 'tarefas/home.html', contexto)

def tarefas_adicionar(request:HttpRequest):

    if request.method == "post" or request.method == "POST":
        formulario = TarefaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect("tarefas:home")


    contexto = {
        "form":TarefaForm
    }
    return render(request, 'tarefas/adicionar.html', contexto)


def tarefas_remover(request:HttpRequest, id):
    tarefa = get_object_or_404(TarefaModel,id=id)
    tarefa.delete()
    return redirect("tarefas:home")