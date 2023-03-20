from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import TodoForm
from .models import Todo

@login_required
def index(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.username = request.user
            todo.save()
            return redirect('dashboard:index')
    else:
        form = TodoForm(initial={'username': request.user})
    todos = Todo.objects.filter(username=request.user)
    return render(request, 'dashboard/index.html', {'form': form, 'todos': todos})

def remove(request, item_id):
    item = Todo.objects.get(id=item_id)
    item.delete()
    return redirect('dashboard:index')

def change_status(request, item_id):
    item = Todo.objects.get(id=item_id)
    if item.completed:
        item.completed = False
    else:
        item.completed = True
    item.save()
    return redirect('dashboard:index')
