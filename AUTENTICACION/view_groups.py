from django.contrib.auth.models import Group
from django.shortcuts import render

def groups_list(request):
    grupos = Group.objects.all()
    
    return render(request, "grupos/lista_grupos.html", {"grupos": grupos})