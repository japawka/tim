from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required



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

# def create(request):
#     form = CreateNewList(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect(all)
#     return render(request, "main/create.html", {"form": form})
@login_required
def create(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            request.user.todolist.add(t)  # adds the to do list to the current logged in user

            return HttpResponseRedirect("/%i" %t.id)

    else:
        form = CreateNewList()
    return render(request, "main/create.html", {"form":form})

def all(request):
    return render(request, "main/all.html", {})
     # todos = ToDoList.objects.all()
     # context = {
     #     'todos': todos
     # }
     # return render(request, 'main/all.html', context)

def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(all)
    return render(request, 'main/register.html', {'form': form})