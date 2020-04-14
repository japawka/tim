from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ToDoList, Item
from .forms import CreateNewList



def index(request, id):
    list = ToDoList.objects.get(id=id)
    items = list.item_set.all()

    if request.method == 'POST':
        if request.POST.get('save'):
            for item in items:
                if request.POST.get('c' + str(item.id)) =='clicked':
                    item.complete = True
                else:
                    item.complete = False
                item.save()

        elif request.POST.get('newItem'):
            txt = request.POST.get('new')

            if len(txt) > 2:
                list.item_set.create(text=txt, complete=False)
            else:
                print("invalid")

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