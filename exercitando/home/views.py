from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def paginahome(request):
    context = { 'h2': 'Página Home'}
    return render(request, 'home/home.html', context)