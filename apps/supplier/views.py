from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)

from .models import Supplier
from .forms import SupplierForm
from .mixins.mixins import BaseSupplierList, SearchConstructMixin, SupplierCreateUpdate

class SupplierListView(BaseSupplierList):
    """
     Display list of Suppliers.
    """

class SupplierCreateView(SupplierCreateUpdate, CreateView):
    success_url = reverse_lazy('supplier:supplier-list')

class SupplierUpdateView(SupplierCreateUpdate, UpdateView):
    context_object_name = 'supplier'

class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'supplier/supplier_detail.html'
    context_object_name = 'supplier'
    login_url = '/'

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    success_url = reverse_lazy('supplier:supplier-list')
    login_url = '/'

class SupplierSearchView(BaseSupplierList, SearchConstructMixin):
    """
    Display search results fort Supplier.
    """

    def get(self, request, **kwargs):
        query = request.GET.get(self.q)
        search_option = request.GET.get(self.search_option)
        if query != '':
            suppliers = self.search_construct(query, search_option)
            context = {'suppliers': suppliers,
                       'query': query,
                       'search_option': search_option,
                       }
            return render(self.request, self.template_name, context)
        else:
            return redirect('supplier:supplier-list')
