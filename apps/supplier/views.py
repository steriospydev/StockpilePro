from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.core.paginator import Paginator

from .models import Supplier
from .forms import SupplierForm

class BaseSupplierList(LoginRequiredMixin, ListView):
    template_name = 'supplier/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 5
    login_url = '/'

    def get_queryset(self):
        active = self.request.GET.get('active')
        if active == 'false':
            return Supplier.objects.filter(is_active=False)
        else:
            return Supplier.active.all()

class SearchConstructMixin:
    q = 'q'
    search_option = 'search_option'

    def search_construct(self, term, option):
        lookup = {
            'Πόλη': 'city__icontains',
            'Τηλέφωνο': 'phone__icontains',
            'ΑΦΜ': 'TIN_num__icontains',
            'Επιχείρηση': 'company__icontains',
            'SKU': 'sku_num__icontains'
        }
        field_lookup = lookup.get(option, None)
        if field_lookup:
            return Supplier.active.filter(**{field_lookup: term})
        else:
            return Supplier.active.all()

class SupplierCreateUpdate(LoginRequiredMixin):
    template_name = 'supplier/supplier_create_update.html'
    model = Supplier
    form_class = SupplierForm
    login_url = '/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

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
