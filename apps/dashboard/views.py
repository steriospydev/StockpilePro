from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import TodoForm
from .models import Todo

from ..invoice.models import Invoice
from ..product.models import Product
from ..supplier.models import Supplier
from ..storehouse.models import Storage

@login_required
def index(request):
    # Count objects
    num_storages = Storage.objects.count()
    num_products = Product.objects.count()
    num_invoices = Invoice.objects.count()
    num_suppliers = Supplier.objects.count()
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
    context = {'form': form, 'todos': todos,
               'num_storages': num_storages,
               'num_products': num_products,
               'num_invoices': num_invoices,
               'num_suppliers': num_suppliers}
    return render(request, 'dashboard/index.html', context)

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
