from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import (ListView,DetailView,
                                  UpdateView,DeleteView)
from django.core.paginator import Paginator

from .models import Supplier
from .forms import SupplierForm

class SupplierListView(LoginRequiredMixin, ListView):
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

# search_experiment branch
class SearchSupplierListView(LoginRequiredMixin, ListView):
    template_name = 'supplier/supplier_list.html'
    context_object_name = 'suppliers'
    login_url = '/'

    def search_construct(self,term, option):
        if option == 'Πόλη':
            return Supplier.active.filter(city__icontains=term)
        elif option == 'Τηλέφωνο':
            return Supplier.active.filter(phone__icontains=term)
        elif option == 'ΑΦΜ':
            return  Supplier.active.filter(TIN_num__icontains=term)
        elif option == 'Επιχείρηση':
            return Supplier.active.filter(company__icontains=term)
        else:
            return Supplier.active.all()

    def get(self, request):
        query = request.GET.get('q')
        search_option = request.GET.get('search_option')
        if query != '':
            suppliers = self.search_construct(query, search_option)
            context = {'suppliers': suppliers,
                       'query':query,
                       'search_option':search_option
                       }
            return render(self.request, self.template_name, context)
        else:
            return redirect('supplier:supplier-list')

class SupplierCreateView(LoginRequiredMixin, View):
    template_name = 'supplier/supplier_create.html'
    success_url = reverse_lazy('supplier:supplier-list')
    login_url = '/'

    def get(self, request):
        context = {
            'supplier_form': SupplierForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        supplier_form = SupplierForm(request.POST)

        if supplier_form.is_valid():
            supplier = supplier_form.save()
            return redirect(self.success_url)
        else:
            context = {'supplier_form': supplier_form}
        return render(request, self.template_name, context)

class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'supplier/supplier_detail.html'
    context_object_name = 'supplier'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = context['supplier']
        return context

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'supplier/supplier_update.html'
    model = Supplier
    form_class = SupplierForm
    context_object_name = 'supplier'
    login_url = '/'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier_form'] = self.form_class(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        supplier_form = self.form_class(request.POST, instance=self.object)

        if supplier_form.is_valid():
            supplier_form.save()
        else:
            return self.render_to_response(self.get_context_data(
                object=object,
                supplier_form=supplier_form
                ))
        return redirect(self.object)

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    success_url = reverse_lazy('supplier:supplier-list')
    login_url = '/'
