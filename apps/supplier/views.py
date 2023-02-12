from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import (ListView,DetailView,
                                  UpdateView,DeleteView)

from django.core.paginator import Paginator

from .models import Supplier, Contact, Address, TIN
from .forms import SupplierForm, TinForm, ContactForm, AddressForm, SupplierUpdateForm

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

class SupplierCreateView(LoginRequiredMixin, View):
    template_name = 'supplier/supplier_create.html'
    success_url = reverse_lazy('supplier:supplier-list')
    login_url = '/'

    def get(self, request):
        context = {
            'supplier_form': SupplierForm(),
            'tin_form': TinForm(prefix='tin'),
            'contact_form': ContactForm(prefix='con'),
            'address_form': AddressForm(prefix='addr')
        }
        return render(request, self.template_name, context)

    def post(self, request):
        supplier_form = SupplierForm(request.POST)
        tin_form = TinForm(request.POST, prefix='tin')
        contact_form = ContactForm(request.POST, prefix='con')
        address_form = AddressForm(request.POST, prefix='addr')

        if supplier_form.is_valid() and tin_form.is_valid() and \
                contact_form.is_valid() and address_form.is_valid():

            supplier = supplier_form.save()

            contact = contact_form.save(commit=False)
            tin = tin_form.save(commit=False)
            address = address_form.save(commit=False)

            contact.supplier = supplier
            tin.supplier = supplier
            address.supplier = supplier

            contact.save()
            tin.save()
            address.save()
            return redirect(self.success_url)
        else:
            context = {'supplier_form': supplier_form, 'tin_form': tin_form,
                       'contact_form': contact_form, 'address_form': address_form}
        return render(request, self.template_name, context)

class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'supplier/supplier_detail.html'
    context_object_name = 'supplier'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier_pk'] = str(self.object.pk)
        supplier = context['supplier']
        address = Address.objects.get(supplier=supplier)
        contact = Contact.objects.get(supplier=supplier)
        tin = TIN.objects.get(supplier=supplier)
        context['address'] = address
        context['contact'] = contact
        context['address'] = address
        context['tin'] = tin
        return context

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'supplier/supplier_update.html'
    model = Supplier
    form_class = SupplierForm
    context_object_name = 'supplier'
    login_url = '/'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        self.tin = TIN.objects.get(supplier=self.object)
        self.contact = Contact.objects.get(supplier=self.object)
        self.address = Address.objects.get(supplier=self.object)
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier_form'] = self.form_class(instance=self.object)
        context['contact_form'] = ContactForm(instance=self.contact)
        context['address_form'] = AddressForm(instance=self.address)
        context['tin_form'] = TinForm(instance=self.tin)
        context['supplier'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        supplier_form = self.form_class(request.POST, instance=self.object)
        contact_form = ContactForm(request.POST, instance=self.contact)
        address_form = AddressForm(request.POST, instance=self.address)
        tin_form = TinForm(request.POST, instance=self.tin)
        forms = [supplier_form, contact_form, address_form, tin_form]
        for form in forms:
            if form.is_valid():
                form.save()
            else:
                return self.render_to_response(self.get_context_data(forms=[
                    supplier_form, contact_form, address_form, tin_form],
                    object=object,
                    supplier_form=supplier_form,
                    contact_form=contact_form,
                    address_form=address_form,
                    tin_form=tin_form))
        return redirect(self.object)

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    success_url = reverse_lazy('supplier:supplier-list')
    login_url = '/'
