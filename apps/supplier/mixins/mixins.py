from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import Supplier
from ..forms import SupplierForm

class BaseSupplierList(LoginRequiredMixin, ListView):
    template_name = 'supplier/supplier_list.html'
    context_object_name = 'suppliers'
    # paginate_by = 5
    login_url = '/'

    def get_queryset(self):
        return Supplier.objects.all()

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
