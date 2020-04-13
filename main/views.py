from django.shortcuts import render
from django.http import HttpResponse
from .models import ToDoList, Item
# Create your views here.

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
