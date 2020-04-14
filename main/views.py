from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ToDoList, Item
from .forms import CreateNewList

def index(request, id):
    list = ToDoList.objects.get(id=id)
    items = list.item_set.all()
    context = {
        'list': list,
        'items': items
    }
    return render(request, 'main/list.html', context)


def home(request):
    return render(request, 'main/home.html', {})

def create(request):
    form = CreateNewList(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(all)
    return render(request, "main/create.html", {"form": form})

def all(request):
     todos = ToDoList.objects.all()
     context = {
         'todos': todos
     }
     return render(request, 'main/all.html', context)