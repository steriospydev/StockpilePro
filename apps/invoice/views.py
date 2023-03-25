from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, get_object_or_404
from django.urls import reverse

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.db.models import Count

from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemForm
from ..product.models import Product

class BaseInvoiceList(LoginRequiredMixin, ListView):
    """
    Base view for displaying a list of invoices.
    """

    model = Invoice
    template_name = 'invoice/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 10
    queryset = Invoice.objects.annotate(
        num_items=Count('id')).select_related('supplier').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_invoices'] = self.queryset.count()
        return context

class InvoiceList(BaseInvoiceList):
    """
    Display all products
    """
    paginate_by = 5

class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'invoice/invoice_detail.html'
    context_object_name = 'invoice'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = self.object  # the current invoice object
        invoice_items = invoice.invoice_items.select_related('product').select_related(
            'product__package').select_related('product__package__material')
        context['invoice_items'] = invoice_items
        return context

class InvoiceItemCreateUpdate(LoginRequiredMixin):
    model = InvoiceItem
    form_class = InvoiceItemForm
    template_name = 'invoice/item_create.html'
    login_url = '/'

    def get_initial(self):
        initial = super().get_initial()
        initial['invoice'] = get_object_or_404(Invoice, id=self.kwargs['invoice_id'])
        return initial

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('product__package',
                                 'product__tax_rate')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.invoice.save()  # call save method on the associated invoice object

        return response

    def get_success_url(self):
        return reverse('invoice:invoice-detail', args=[self.object.invoice.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = get_object_or_404(Invoice, id=self.kwargs['invoice_id'])
        return context

class InvoiceItemCreateView(InvoiceItemCreateUpdate, CreateView):
    pass

class InvoiceItemUpdateView(InvoiceItemCreateUpdate, UpdateView):
    context_object_name = 'item'


@login_required(login_url='/')
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            return redirect('invoice:invoice-list')
    else:
        form = InvoiceForm()
    return render(request, 'invoice/invoice_create.html', {'form': form})
